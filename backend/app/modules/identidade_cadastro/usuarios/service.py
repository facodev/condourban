import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.modules.identidade_cadastro.pessoas.models import Pessoa
from .models import MembroCondominio, OcupacaoUnidade, Usuario
from .schemas import (
    OcupacaoUnidadeCreate,
    OcupacaoUnidadeUpdate,
    RotinaExpiracaoResponse,
    Token,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse,
    UsuarioUpdate,
)


class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_usuarios(
        self, condominio_id: uuid.UUID | None = None
    ) -> list[Usuario]:
        if not condominio_id:
            c_info = self.db.info.get('condominio_id')
            if c_info:
                try:
                    condominio_id = uuid.UUID(str(c_info))
                except (ValueError, TypeError):
                    pass

        if not condominio_id:
            stmt = select(Usuario).order_by(Usuario.criado_em.desc())
            result = await self.db.execute(stmt)
            users = list(result.scalars().all())
            for user in users:
                user.ativo = user.status == 'ATIVO'
                user.papeis = ['ADMINISTRADOR'] if user.status == 'ATIVO' else []
                if user.pessoa_id:
                    pessoa = (
                        await self.db.execute(
                            select(Pessoa).where(Pessoa.id == user.pessoa_id)
                        )
                    ).scalar_one_or_none()
                    if pessoa:
                        user.nome_completo = pessoa.nome_completo
                        user.nome = pessoa.nome_completo
            return users

        # Join com MembroCondominio para listar apenas usuários que pertencem ao condomínio ativo
        stmt = (
            select(Usuario)
            .join(MembroCondominio, MembroCondominio.pessoa_id == Usuario.pessoa_id)
            .where(
                MembroCondominio.condominio_id == condominio_id,
                MembroCondominio.status == 'ATIVO'
            )
            .distinct()
            .order_by(Usuario.criado_em.desc())
        )
        result = await self.db.execute(stmt)
        users = list(result.scalars().all())

        for user in users:
            user.ativo = user.status == 'ATIVO'
            papeis: list[str] = []

            if user.pessoa_id:
                pessoa = (
                    await self.db.execute(
                        select(Pessoa).where(Pessoa.id == user.pessoa_id)
                    )
                ).scalar_one_or_none()
                if pessoa:
                    user.nome_completo = pessoa.nome_completo
                    user.nome = pessoa.nome_completo

                # Buscar papéis do membro no condomínio ativo
                m_query = select(MembroCondominio).where(
                    MembroCondominio.pessoa_id == user.pessoa_id,
                    MembroCondominio.condominio_id == condominio_id,
                    MembroCondominio.status == 'ATIVO',
                )
                membros = (await self.db.execute(m_query)).scalars().all()
                papeis = [m.tipo_pessoa for m in membros]

            if not papeis:
                papeis = ['MORADOR']
            user.papeis = papeis
            user.roles = papeis
            user.condominio_id = condominio_id

        return users

    async def get_usuario(self, user_id: uuid.UUID) -> Usuario:
        user = await self.db.get(Usuario, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='USUARIO_NAO_ENCONTRADO',
            )
        user.ativo = user.status == 'ATIVO'
        papeis: list[str] = []
        if user.pessoa_id:
            pessoa = await self.db.get(Pessoa, user.pessoa_id)
            if pessoa:
                user.nome_completo = pessoa.nome_completo
                user.nome = pessoa.nome_completo
            membros = (
                await self.db.execute(
                    select(MembroCondominio).where(
                        MembroCondominio.pessoa_id == user.pessoa_id,
                        MembroCondominio.status == 'ATIVO',
                    )
                )
            ).scalars().all()
            papeis = [m.tipo_pessoa for m in membros]
        if not papeis:
            papeis = ['MORADOR']
        user.papeis = papeis
        user.roles = papeis
        return user

    async def create_usuario(self, dto: UsuarioCreate, condominio_id: uuid.UUID | None = None) -> Usuario:
        query = select(Usuario).where(Usuario.email == dto.email)
        existing = (await self.db.execute(query)).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email já cadastrado',
            )

        pessoa_id = dto.pessoa_id
        target_condo_id = dto.condominio_id or condominio_id

        senha = dto.senha or 'Condo@123'
        user = Usuario(
            email=dto.email,
            senha_hash=get_password_hash(senha),
            pessoa_id=pessoa_id,
            status='ATIVO',
        )
        self.db.add(user)
        await self.db.flush()

        # Vincular membro condomínio com o papel especificado
        papel = dto.papel_sistema or dto.papel or 'MORADOR'
        if target_condo_id and pessoa_id:
            membro = MembroCondominio(
                id=uuid.uuid4(),
                condominio_id=target_condo_id,
                pessoa_id=pessoa_id,
                tipo_pessoa=papel.upper(),
                status='ATIVO',
            )
            self.db.add(membro)

        await self.db.commit()
        await self.db.refresh(user)

        user.nome_completo = dto.nome_completo
        user.nome = dto.nome_completo
        user.papeis = [papel.upper()]
        user.roles = [papel.upper()]
        user.ativo = True
        return user

    async def update_usuario(
        self, user_id: uuid.UUID, dto: UsuarioUpdate, condominio_id: uuid.UUID | None = None
    ) -> Usuario:
        user = await self.get_usuario(user_id)

        if dto.email is not None and dto.email != user.email:
            dup = (
                await self.db.execute(
                    select(Usuario).where(Usuario.email == dto.email, Usuario.id != user_id)
                )
            ).scalar_one_or_none()
            if dup:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email já está em uso por outro usuário',
                )
            user.email = dto.email

        if dto.senha:
            user.senha_hash = get_password_hash(dto.senha)

        if dto.status is not None:
            user.status = dto.status
        elif dto.ativo is not None:
            user.status = 'ATIVO' if dto.ativo else 'INATIVO'

        if dto.pessoa_id is not None:
            user.pessoa_id = dto.pessoa_id

        target_condo_id = dto.condominio_id or condominio_id

        # Atualiza nome da pessoa vinculada se fornecido
        if dto.nome_completo:
            if user.pessoa_id:
                pessoa = await self.db.get(Pessoa, user.pessoa_id)
                if pessoa:
                    pessoa.nome_completo = dto.nome_completo
            else:
                nova_pessoa = Pessoa(
                    id=uuid.uuid4(),
                    nome_completo=dto.nome_completo,
                    email=user.email,
                )
                self.db.add(nova_pessoa)
                await self.db.flush()
                user.pessoa_id = nova_pessoa.id

        # Atualizar papel no MembroCondominio
        papel = dto.papel_sistema or dto.papel
        if papel and user.pessoa_id:
            m_stmt = select(MembroCondominio).where(
                MembroCondominio.pessoa_id == user.pessoa_id
            )
            if target_condo_id:
                m_stmt = m_stmt.where(MembroCondominio.condominio_id == target_condo_id)
            membro = (await self.db.execute(m_stmt)).scalars().first()
            if membro:
                membro.tipo_pessoa = papel.upper()
                membro.status = user.status
            elif target_condo_id:
                novo_m = MembroCondominio(
                    id=uuid.uuid4(),
                    condominio_id=target_condo_id,
                    pessoa_id=user.pessoa_id,
                    tipo_pessoa=papel.upper(),
                    status='ATIVO',
                )
                self.db.add(novo_m)

        await self.db.commit()
        await self.db.refresh(user)

        user.nome_completo = dto.nome_completo or getattr(user, 'nome_completo', None)
        user.nome = user.nome_completo
        if papel:
            user.papeis = [papel.upper()]
            user.roles = [papel.upper()]
        user.ativo = user.status == 'ATIVO'
        return user

    async def delete_usuario(self, user_id: uuid.UUID) -> dict:
        user = await self.db.get(Usuario, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='USUARIO_NAO_ENCONTRADO',
            )

        # Se for membro, inativar membros
        if user.pessoa_id:
            membros = (
                await self.db.execute(
                    select(MembroCondominio).where(MembroCondominio.pessoa_id == user.pessoa_id)
                )
            ).scalars().all()
            for m in membros:
                await self.db.delete(m)

        await self.db.delete(user)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': 'Usuário removido com sucesso.'}

    async def authenticate(self, dto: UsuarioLogin) -> Token:
        query = select(Usuario).where(Usuario.email == dto.email)
        user = (await self.db.execute(query)).scalar_one_or_none()
        if not user or not verify_password(dto.senha, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Credenciais inválidas',
            )
        token = create_access_token(subject=str(user.id))
        return Token(access_token=token)


class OcupacaoUnidadeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def listar_ocupacoes(
        self,
        unidade_id: uuid.UUID | None = None,
        condominio_id: uuid.UUID | None = None,
        apenas_ativas: bool = False,
        unidade_ids: list[uuid.UUID] | None = None,
    ) -> list[OcupacaoUnidade]:
        query = select(OcupacaoUnidade)
        if unidade_id:
            query = query.where(OcupacaoUnidade.unidade_id == unidade_id)
        if unidade_ids is not None:
            if not unidade_ids:
                return []
            query = query.where(OcupacaoUnidade.unidade_id.in_(unidade_ids))
        if condominio_id:
            query = query.where(OcupacaoUnidade.condominio_id == condominio_id)
        if apenas_ativas:
            now = datetime.now(timezone.utc)
            query = query.where(
                OcupacaoUnidade.status.in_(['ATIVO', 'ATIVA']),
                (OcupacaoUnidade.fim_em.is_(None)) | (OcupacaoUnidade.fim_em > now),
            )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def obter_ocupacao(self, ocupacao_id: uuid.UUID) -> OcupacaoUnidade:
        ocupacao = await self.db.get(OcupacaoUnidade, ocupacao_id)
        if not ocupacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='OCUPACAO_NAO_ENCONTRADA',
            )
        return ocupacao

    async def criar_ocupacao(
        self, dto: OcupacaoUnidadeCreate, condominio_id: uuid.UUID | None = None
    ) -> OcupacaoUnidade:
        now = datetime.now(timezone.utc)
        c_id = condominio_id or dto.condominio_id
        if not c_id:
            from app.modules.condominio.estrutura.models import Condominio, Unidade
            u = (await self.db.execute(select(Unidade).where(Unidade.id == dto.unidade_id))).scalar_one_or_none()
            if u and u.condominio_id:
                c_id = u.condominio_id
            else:
                first_c = (await self.db.execute(select(Condominio))).scalars().first()
                c_id = first_c.id if first_c else uuid.uuid4()

        # Garantir vínculo em MembroCondominio para o condomínio ativo
        m_stmt = select(MembroCondominio).where(
            MembroCondominio.pessoa_id == dto.pessoa_id,
            MembroCondominio.condominio_id == c_id,
        )
        membro = (await self.db.execute(m_stmt)).scalar_one_or_none()
        if not membro:
            membro = MembroCondominio(
                condominio_id=c_id,
                pessoa_id=dto.pessoa_id,
                tipo_pessoa=dto.tipo_vinculo or 'MORADOR',
                status='ATIVO',
            )
            self.db.add(membro)
            await self.db.flush()

        # Regra 1: Conflito de Posse Direta (Proprietário Morador vs. Inquilino)
        # Se for PROPRIETARIO com mora_no_local = True, não pode haver INQUILINO ativo
        if dto.tipo_vinculo == 'PROPRIETARIO' and dto.mora_no_local:
            query_inq = select(OcupacaoUnidade).where(
                OcupacaoUnidade.unidade_id == dto.unidade_id,
                OcupacaoUnidade.tipo_vinculo == 'INQUILINO',
                OcupacaoUnidade.status == 'ATIVO',
                (OcupacaoUnidade.fim_em.is_(None)) | (OcupacaoUnidade.fim_em > now),
            )
            inq_existente = (await self.db.execute(query_inq)).scalar_one_or_none()
            if inq_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='CONFLITO_POSSE_DIRETA: Unidade possui inquilino ativo; proprietário não pode constar como morador local.',
                )

        # Se for INQUILINO ATIVO, desmarca automaticamente mora_no_local dos proprietários daquela unidade
        if dto.tipo_vinculo == 'INQUILINO':
            query_prop = select(OcupacaoUnidade).where(
                OcupacaoUnidade.unidade_id == dto.unidade_id,
                OcupacaoUnidade.tipo_vinculo == 'PROPRIETARIO',
                OcupacaoUnidade.mora_no_local.is_(True),
                OcupacaoUnidade.status == 'ATIVO',
            )
            props = (await self.db.execute(query_prop)).scalars().all()
            for p in props:
                p.mora_no_local = False
                p.atualizado_em = now

        # Regra 5: Dependentes exigem um responsável morador (PROPRIETARIO morador ou INQUILINO ativo)
        if dto.tipo_vinculo == 'DEPENDENTE':
            if dto.responsavel_ocupacao_id:
                resp = await self.db.get(OcupacaoUnidade, dto.responsavel_ocupacao_id)
                if (
                    not resp
                    or resp.unidade_id != dto.unidade_id
                    or resp.status != 'ATIVO'
                    or not resp.mora_no_local
                    or resp.tipo_vinculo not in ('PROPRIETARIO', 'INQUILINO')
                    or (resp.fim_em and resp.fim_em <= now)
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='DEPENDENTE_SEM_RESPONSAVEL_RESIDENTE: O responsável informado deve ser um proprietário morador ou inquilino ativo na mesma unidade.',
                    )
            else:
                query_resp = select(OcupacaoUnidade).where(
                    OcupacaoUnidade.unidade_id == dto.unidade_id,
                    OcupacaoUnidade.tipo_vinculo.in_(['PROPRIETARIO', 'INQUILINO']),
                    OcupacaoUnidade.mora_no_local.is_(True),
                    OcupacaoUnidade.status == 'ATIVO',
                    (OcupacaoUnidade.fim_em.is_(None)) | (OcupacaoUnidade.fim_em > now),
                )
                resp_existente = (await self.db.execute(query_resp)).scalar_one_or_none()
                if not resp_existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='DEPENDENTE_SEM_RESPONSAVEL_RESIDENTE: Registros de dependente exigem pelo menos um proprietário morador ou inquilino ativo e residente na mesma unidade.',
                    )

        nova_ocupacao = OcupacaoUnidade(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            pessoa_id=dto.pessoa_id,
            tipo_vinculo=dto.tipo_vinculo,
            mora_no_local=dto.mora_no_local,
            principal=dto.principal,
            responsavel_ocupacao_id=dto.responsavel_ocupacao_id,
            inicio_em=dto.inicio_em or now,
            fim_em=dto.fim_em,
            status='ATIVO',
        )
        self.db.add(nova_ocupacao)
        await self.db.commit()
        await self.db.refresh(nova_ocupacao)
        return nova_ocupacao

    async def atualizar_ocupacao(
        self, ocupacao_id: uuid.UUID, dto: OcupacaoUnidadeUpdate
    ) -> OcupacaoUnidade:
        ocupacao = await self.obter_ocupacao(ocupacao_id)
        now = datetime.now(timezone.utc)

        novo_tipo = dto.tipo_vinculo or ocupacao.tipo_vinculo
        novo_mora = dto.mora_no_local if dto.mora_no_local is not None else ocupacao.mora_no_local
        novo_status = dto.status or ocupacao.status

        # Regra 1 na atualização
        if novo_status == 'ATIVO' and novo_tipo == 'PROPRIETARIO' and novo_mora:
            query_inq = select(OcupacaoUnidade).where(
                OcupacaoUnidade.unidade_id == ocupacao.unidade_id,
                OcupacaoUnidade.tipo_vinculo == 'INQUILINO',
                OcupacaoUnidade.status == 'ATIVO',
                OcupacaoUnidade.id != ocupacao.id,
                (OcupacaoUnidade.fim_em.is_(None)) | (OcupacaoUnidade.fim_em > now),
            )
            inq_existente = (await self.db.execute(query_inq)).scalar_one_or_none()
            if inq_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='CONFLITO_POSSE_DIRETA: Unidade possui inquilino ativo; proprietário não pode constar como morador local.',
                )

        if novo_status == 'ATIVO' and novo_tipo == 'INQUILINO':
            query_prop = select(OcupacaoUnidade).where(
                OcupacaoUnidade.unidade_id == ocupacao.unidade_id,
                OcupacaoUnidade.tipo_vinculo == 'PROPRIETARIO',
                OcupacaoUnidade.mora_no_local.is_(True),
                OcupacaoUnidade.status == 'ATIVO',
                OcupacaoUnidade.id != ocupacao.id,
            )
            props = (await self.db.execute(query_prop)).scalars().all()
            for p in props:
                p.mora_no_local = False
                p.atualizado_em = now

        # Regra 2 na atualização
        inicio = dto.inicio_em or ocupacao.inicio_em
        fim = dto.fim_em if dto.fim_em is not None else ocupacao.fim_em
        if novo_tipo in ('TEMPORARIO', 'HOSPEDE'):
            if not inicio or not fim:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='DATAS_OBRIGATORIAS_CURTO_PRAZO: Para vínculos TEMPORARIO ou HOSPEDE, as datas de início e fim são obrigatórias.',
                )

        # Regra 3 na atualização
        if inicio and fim and fim <= inicio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='DATA_FIM_DEVE_SER_MAIOR_QUE_INICIO: A data_fim deve ser estritamente maior que a data_inicio.',
            )

        if dto.unidade_id is not None:
            ocupacao.unidade_id = dto.unidade_id
            from app.modules.condominio.estrutura.models import Unidade
            u_res = (await self.db.execute(select(Unidade).where(Unidade.id == dto.unidade_id))).scalar_one_or_none()
            if u_res and u_res.condominio_id:
                ocupacao.condominio_id = u_res.condominio_id
        if dto.tipo_vinculo is not None:
            ocupacao.tipo_vinculo = dto.tipo_vinculo
        if dto.mora_no_local is not None:
            ocupacao.mora_no_local = dto.mora_no_local
        if dto.principal is not None:
            ocupacao.principal = dto.principal
        if dto.responsavel_ocupacao_id is not None:
            ocupacao.responsavel_ocupacao_id = dto.responsavel_ocupacao_id
        if dto.inicio_em is not None:
            ocupacao.inicio_em = dto.inicio_em
        if dto.fim_em is not None:
            ocupacao.fim_em = dto.fim_em
        if dto.status is not None:
            ocupacao.status = dto.status

        ocupacao.atualizado_em = now
        await self.db.commit()
        await self.db.refresh(ocupacao)
        return ocupacao

    async def inativar_ocupacao(
        self,
        ocupacao_id: uuid.UUID,
        cascade_dependentes: bool = True,
        novo_responsavel_ocupacao_id: uuid.UUID | None = None,
    ) -> dict:
        ocupacao = await self.obter_ocupacao(ocupacao_id)
        now = datetime.now(timezone.utc)
        ocupacao.status = 'INATIVO'
        ocupacao.atualizado_em = now

        dependentes_afetados = 0
        # Regra 5: Cascade nos dependentes
        if ocupacao.tipo_vinculo in ('INQUILINO', 'PROPRIETARIO'):
            query_dep = select(OcupacaoUnidade).where(
                OcupacaoUnidade.status == 'ATIVO',
                (OcupacaoUnidade.responsavel_ocupacao_id == ocupacao.id)
                | (
                    (OcupacaoUnidade.unidade_id == ocupacao.unidade_id)
                    & (OcupacaoUnidade.tipo_vinculo == 'DEPENDENTE')
                ),
            )
            deps = (await self.db.execute(query_dep)).scalars().all()

            # Checar se ainda resta outro titular residente ativo na unidade
            query_outros = select(OcupacaoUnidade).where(
                OcupacaoUnidade.unidade_id == ocupacao.unidade_id,
                OcupacaoUnidade.tipo_vinculo.in_(['PROPRIETARIO', 'INQUILINO']),
                OcupacaoUnidade.mora_no_local.is_(True),
                OcupacaoUnidade.status == 'ATIVO',
                OcupacaoUnidade.id != ocupacao.id,
                (OcupacaoUnidade.fim_em.is_(None)) | (OcupacaoUnidade.fim_em > now),
            )
            outro_titular = (await self.db.execute(query_outros)).scalar_one_or_none()

            for d in deps:
                if novo_responsavel_ocupacao_id:
                    d.responsavel_ocupacao_id = novo_responsavel_ocupacao_id
                    d.atualizado_em = now
                elif cascade_dependentes or not outro_titular:
                    d.status = 'INATIVO'
                    d.atualizado_em = now
                    dependentes_afetados += 1

        await self.db.commit()
        await self.db.refresh(ocupacao)
        return {
            'ocupacao_id': str(ocupacao.id),
            'status': ocupacao.status,
            'dependentes_inativados': dependentes_afetados,
        }

    async def executar_rotina_expiracao(
        self, condominio_id: uuid.UUID | None = None
    ) -> RotinaExpiracaoResponse:
        now = datetime.now(timezone.utc)
        query = select(OcupacaoUnidade).where(
            OcupacaoUnidade.status == 'ATIVO',
            OcupacaoUnidade.fim_em.is_not(None),
            OcupacaoUnidade.fim_em < now,
        )
        if condominio_id:
            query = query.where(OcupacaoUnidade.condominio_id == condominio_id)

        expirados = list((await self.db.execute(query)).scalars().all())
        total_ocupacoes = 0
        total_dependentes = 0

        for exp in expirados:
            res = await self.inativar_ocupacao(exp.id, cascade_dependentes=True)
            total_ocupacoes += 1
            total_dependentes += res['dependentes_inativados']

        return RotinaExpiracaoResponse(
            ocupacoes_inativadas=total_ocupacoes,
            dependentes_inativados=total_dependentes,
        )


# Aliases de retrocompatibilidade
UserService = UsuarioService
