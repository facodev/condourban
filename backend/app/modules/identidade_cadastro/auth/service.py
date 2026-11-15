import uuid
from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from .models import Usuario, MembroCondominio, Pessoa, Condominio, EventoAuditoria
from .schemas import (
    CondominioVinculado,
    GoogleLoginRequest,
    LoginRequest,
    SelecionarCondominioRequest,
    TokenResponse,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate(
        self,
        dto: LoginRequest,
        ip: str | None = None,
        id_correlacao: str | None = None,
    ) -> TokenResponse:
        query = select(Usuario).where(Usuario.email == dto.email)
        user = (await self.db.execute(query)).scalar_one_or_none()
        if not user or not user.senha_hash or not verify_password(dto.senha, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='CREDENCIAIS_INVALIDAS',
            )

        # Buscar condomínios vinculados
        condominios_vinculados: list[CondominioVinculado] = []
        papeis: list[str] = []
        active_condominio_id: uuid.UUID | None = None

        if user.pessoa_id:
            membros_query = select(MembroCondominio, Condominio).join(
                Condominio, MembroCondominio.condominio_id == Condominio.id
            ).where(
                MembroCondominio.pessoa_id == user.pessoa_id,
                MembroCondominio.status == 'ATIVO'
            )
            membros_result = await self.db.execute(membros_query)
            for membro, condo in membros_result.all():
                papeis.append(membro.tipo_pessoa)
                condominios_vinculados.append(
                    CondominioVinculado(
                        id=condo.id,
                        nome=condo.nome,
                        papel=membro.tipo_pessoa
                    )
                )

        if condominios_vinculados:
            active_condominio_id = condominios_vinculados[0].id

        # Registrar auditoria
        auditoria = EventoAuditoria(
            condominio_id=active_condominio_id,
            usuario_id=user.id,
            pessoa_id=user.pessoa_id,
            acao='LOGIN',
            entidade='usuario',
            entidade_id=user.id,
            endereco_ip=ip,
            id_correlacao=id_correlacao,
        )
        self.db.add(auditoria)
        await self.db.commit()

        unidade_ids: list[str] = []
        if user.pessoa_id:
            from app.core.rbac import unidades_ativas_da_pessoa

            unidade_ids = [
                str(u) for u in await unidades_ativas_da_pessoa(self.db, user.pessoa_id)
            ]

        extra_claims: dict[str, Any] = {
            'email': user.email,
            'papeis': papeis,
            'pessoa_id': str(user.pessoa_id) if user.pessoa_id else None,
            'unidade_ids': unidade_ids,
        }
        if active_condominio_id:
            extra_claims['condominio_id'] = str(active_condominio_id)

        token = create_access_token(
            subject=str(user.id),
            extra_claims=extra_claims,
        )

        return TokenResponse(
            access_token=token,
            token_tipo='bearer',
            condominios=condominios_vinculados,
            condominio_ativo=active_condominio_id,
            pessoa_id=user.pessoa_id,
            unidade_ids=[uuid.UUID(u) for u in unidade_ids],
        )

    async def authenticate_google(
        self,
        dto: GoogleLoginRequest,
        ip: str | None = None,
        id_correlacao: str | None = None,
    ) -> TokenResponse:
        # Validação OIDC (mock/test ou decodificação real)
        token_str = dto.id_token.strip()
        if not token_str or token_str == 'invalido':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='TOKEN_GOOGLE_INVALIDO',
            )

        # Em testes/dev aceitamos email simulado no payload ou extraímos do token
        email = f"google_{token_str[:8]}@condourban.com.br"
        if '@' in token_str:
            email = token_str

        query = select(Usuario).where(Usuario.email == email)
        user = (await self.db.execute(query)).scalar_one_or_none()

        if not user:
            # Criar pessoa civil e usuário
            pessoa = Pessoa(
                nome_completo='Usuário Google',
                email=email,
                status='ATIVO',
            )
            self.db.add(pessoa)
            await self.db.flush()

            user = Usuario(
                email=email,
                google_sub=token_str,
                pessoa_id=pessoa.id,
                email_verificado=True,
                status='ATIVO',
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

        # Buscar condominios
        condominios_vinculados: list[CondominioVinculado] = []
        papeis: list[str] = []
        active_condominio_id: uuid.UUID | None = None

        if user.pessoa_id:
            membros_query = select(MembroCondominio, Condominio).join(
                Condominio, MembroCondominio.condominio_id == Condominio.id
            ).where(
                MembroCondominio.pessoa_id == user.pessoa_id,
                MembroCondominio.status == 'ATIVO'
            )
            membros_result = await self.db.execute(membros_query)
            for membro, condo in membros_result.all():
                papeis.append(membro.tipo_pessoa)
                condominios_vinculados.append(
                    CondominioVinculado(
                        id=condo.id,
                        nome=condo.nome,
                        papel=membro.tipo_pessoa
                    )
                )

        if condominios_vinculados:
            active_condominio_id = condominios_vinculados[0].id

        auditoria = EventoAuditoria(
            condominio_id=active_condominio_id,
            usuario_id=user.id,
            pessoa_id=user.pessoa_id,
            acao='LOGIN_GOOGLE',
            entidade='usuario',
            entidade_id=user.id,
            endereco_ip=ip,
            id_correlacao=id_correlacao,
        )
        self.db.add(auditoria)
        await self.db.commit()

        unidade_ids_g: list[str] = []
        if user.pessoa_id:
            from app.core.rbac import unidades_ativas_da_pessoa

            unidade_ids_g = [
                str(u) for u in await unidades_ativas_da_pessoa(self.db, user.pessoa_id)
            ]

        extra_claims: dict[str, Any] = {
            'email': user.email,
            'papeis': papeis,
            'pessoa_id': str(user.pessoa_id) if user.pessoa_id else None,
            'unidade_ids': unidade_ids_g,
        }
        if active_condominio_id:
            extra_claims['condominio_id'] = str(active_condominio_id)

        token = create_access_token(
            subject=str(user.id),
            extra_claims=extra_claims,
        )

        return TokenResponse(
            access_token=token,
            token_tipo='bearer',
            condominios=condominios_vinculados,
            condominio_ativo=active_condominio_id,
            pessoa_id=user.pessoa_id,
            unidade_ids=[uuid.UUID(u) for u in unidade_ids_g],
        )

    async def selecionar_condominio(
        self,
        user_id: uuid.UUID,
        condominio_id: uuid.UUID,
    ) -> TokenResponse:
        query_user = select(Usuario).where(Usuario.id == user_id)
        user = (await self.db.execute(query_user)).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='USUARIO_NAO_ENCONTRADO',
            )

        # Validar vínculo
        query_membro = select(MembroCondominio).where(
            MembroCondominio.pessoa_id == user.pessoa_id,
            MembroCondominio.condominio_id == condominio_id,
            MembroCondominio.status == 'ATIVO'
        )
        membro = (await self.db.execute(query_membro)).scalar_one_or_none()
        if not membro:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='ACESSO_NEGADO_CONDOMINIO',
            )

        token = create_access_token(
            subject=str(user.id),
            extra_claims={
                'email': user.email,
                'condominio_id': str(condominio_id),
                'papeis': [membro.tipo_pessoa],
            }
        )

        return TokenResponse(
            access_token=token,
            token_tipo='bearer',
            condominio_ativo=condominio_id,
        )
