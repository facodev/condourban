import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identidade_cadastro.pessoas.models import Pessoa
from app.modules.identidade_cadastro.usuarios.models import (
    MembroCondominio,
    OcupacaoUnidade,
)
from app.core.security import create_magic_link_token, decode_magic_link_token
from .models import ConviteCadastroMorador, SolicitacaoCadastroMorador
from .schemas import (
    AprovarSolicitacaoRequest,
    ConfirmarMagicLinkRequest,
    ConfirmarMagicLinkResponse,
    ConviteEnvioRequest,
    ConviteEnvioResponse,
    RejeitarSolicitacaoRequest,
    RevogarVinculoRequest,
    RevogarVinculoResponse,
    SolicitacaoAprovacaoResponse,
    SolicitacaoCadastroResponse,
    SolicitacaoIngressoRequest,
    SolicitacaoRejeicaoResponse,
    VerificarCpfOnboardingRequest,
    VerificarCpfOnboardingResponse,
)


class OnboardingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def criar_convite(
        self,
        dto: ConviteEnvioRequest,
        autor_id: uuid.UUID | None = None,
    ) -> ConviteEnvioResponse:
        c_id = dto.condominio_id or uuid.uuid4()
        token = secrets.token_urlsafe(32)
        validade_em = datetime.now(timezone.utc) + timedelta(days=7)

        convite = ConviteCadastroMorador(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            tipo_vinculo=dto.tipo_vinculo,
            token_hash=token,
            codigo=token[:8].upper(),
            validade_em=validade_em,
            criado_por=autor_id,
            status='ATIVO',
        )
        self.db.add(convite)
        await self.db.commit()
        await self.db.refresh(convite)

        return ConviteEnvioResponse(
            convite_id=convite.id,
            token=token,
            expira_em=validade_em,
            unidade_id=convite.unidade_id,
        )

    async def aceitar_convite(self, token: str) -> dict:
        query = select(ConviteCadastroMorador).where(
            ConviteCadastroMorador.token_hash == token
        )
        convite = (await self.db.execute(query)).scalar_one_or_none()
        if not convite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='CONVITE_NAO_ENCONTRADO',
            )

        now = datetime.now(timezone.utc)
        validade = convite.validade_em
        if validade.tzinfo is None:
            validade = validade.replace(tzinfo=timezone.utc)

        if validade < now or convite.status in ('EXPIRADO', 'USADO'):
            if convite.status != 'USADO':
                convite.status = 'EXPIRADO'
                await self.db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='CONVITE_EXPIRADO',
            )

        convite.status = 'USADO'
        convite.usado_em = now
        await self.db.commit()
        return {
            'status': 'ACEITO',
            'unidade_id': convite.unidade_id,
            'tipo_vinculo': convite.tipo_vinculo,
        }

    async def solicitar_cadastro(
        self, dto: SolicitacaoIngressoRequest
    ) -> SolicitacaoCadastroResponse:
        # Se houver convite, valida se é válido
        condominio_id = dto.condominio_id
        if dto.convite_id:
            convite = (
                await self.db.execute(
                    select(ConviteCadastroMorador).where(
                        ConviteCadastroMorador.id == dto.convite_id
                    )
                )
            ).scalar_one_or_none()
            if convite:
                condominio_id = convite.condominio_id

        if not condominio_id:
            condominio_id = uuid.uuid4()

        # Localiza ou cria a Pessoa civil
        pessoa_query = select(Pessoa).where(Pessoa.email == dto.email)
        pessoa = (await self.db.execute(pessoa_query)).scalar_one_or_none()
        if not pessoa:
            from app.modules.condominio.estrutura.models import Condominio
            cond_res = (
                await self.db.execute(
                    select(Condominio.inquilino_id).where(Condominio.id == condominio_id)
                )
            ).scalar_one_or_none()
            inquilino_id = cond_res or condominio_id

            pessoa = Pessoa(
                inquilino_id=inquilino_id,
                nome_completo=dto.nome_completo,
                email=dto.email,
                celular=dto.celular,
            )
            self.db.add(pessoa)
            await self.db.flush()

        solicitacao = SolicitacaoCadastroMorador(
            condominio_id=condominio_id,
            unidade_id=dto.unidade_id,
            convite_id=dto.convite_id,
            pessoa_id=pessoa.id,
            tipo_vinculo=dto.tipo_vinculo,
            status='ENVIADA',
            etapa_atual='VALIDACAO_DOCUMENTAL',
            enviada_em=datetime.now(timezone.utc),
        )
        self.db.add(solicitacao)
        await self.db.commit()
        await self.db.refresh(solicitacao)

        return SolicitacaoCadastroResponse.model_validate(solicitacao)

    async def listar_solicitacoes(
        self,
        condominio_id: uuid.UUID | None = None,
        status_filtro: str | None = None,
    ) -> list[SolicitacaoCadastroResponse]:
        stmt = select(SolicitacaoCadastroMorador)
        if condominio_id:
            stmt = stmt.where(SolicitacaoCadastroMorador.condominio_id == condominio_id)
        if status_filtro:
            stmt = stmt.where(SolicitacaoCadastroMorador.status == status_filtro)
        stmt = stmt.order_by(SolicitacaoCadastroMorador.criada_em.desc())
        result = await self.db.execute(stmt)
        return [
            SolicitacaoCadastroResponse.model_validate(s)
            for s in result.scalars().all()
        ]

    async def aprovar_solicitacao(
        self,
        solicitacao_id: uuid.UUID,
        dto: AprovarSolicitacaoRequest,
        analisado_por: uuid.UUID | None = None,
    ) -> SolicitacaoAprovacaoResponse:
        stmt = select(SolicitacaoCadastroMorador).where(
            SolicitacaoCadastroMorador.id == solicitacao_id
        )
        solicitacao = (await self.db.execute(stmt)).scalar_one_or_none()
        if not solicitacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='SOLICITACAO_NAO_ENCONTRADA',
            )

        if solicitacao.status in ('APROVADA', 'REJEITADA'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'SOLICITACAO_JA_{solicitacao.status}',
            )

        now = datetime.now(timezone.utc)
        solicitacao.status = 'APROVADA'
        solicitacao.analisada_em = now
        solicitacao.analisada_por = analisado_por
        solicitacao.observacao_administrador = dto.observacao

        # Garante criação/reativação do MembroCondominio
        m_stmt = select(MembroCondominio).where(
            MembroCondominio.pessoa_id == solicitacao.pessoa_id,
            MembroCondominio.condominio_id == solicitacao.condominio_id,
        )
        membro = (await self.db.execute(m_stmt)).scalar_one_or_none()
        if not membro:
            membro = MembroCondominio(
                condominio_id=solicitacao.condominio_id,
                pessoa_id=solicitacao.pessoa_id,
                tipo_pessoa=solicitacao.tipo_vinculo or 'MORADOR',
                status='ATIVO',
            )
            self.db.add(membro)
        else:
            membro.status = 'ATIVO'

        # Cria ocupação de unidade automática
        ocupacao = OcupacaoUnidade(
            condominio_id=solicitacao.condominio_id,
            unidade_id=solicitacao.unidade_id,
            pessoa_id=solicitacao.pessoa_id,
            tipo_vinculo=solicitacao.tipo_vinculo,
            mora_no_local=True,
            status='ATIVO',
            inicio_em=now,
        )
        self.db.add(ocupacao)
        await self.db.commit()
        await self.db.refresh(solicitacao)
        await self.db.refresh(ocupacao)

        return SolicitacaoAprovacaoResponse(
            solicitacao_id=solicitacao.id,
            status=solicitacao.status,
            aprovado_em=now,
            ocupacao_id=ocupacao.id,
        )

    async def rejeitar_solicitacao(
        self,
        solicitacao_id: uuid.UUID,
        dto: RejeitarSolicitacaoRequest,
        analisado_por: uuid.UUID | None = None,
    ) -> SolicitacaoRejeicaoResponse:
        if not dto.motivo_rejeicao or not dto.motivo_rejeicao.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='MOTIVO_REJEICAO_OBRIGATORIO',
            )

        stmt = select(SolicitacaoCadastroMorador).where(
            SolicitacaoCadastroMorador.id == solicitacao_id
        )
        solicitacao = (await self.db.execute(stmt)).scalar_one_or_none()
        if not solicitacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='SOLICITACAO_NAO_ENCONTRADA',
            )

        if solicitacao.status in ('APROVADA', 'REJEITADA'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'SOLICITACAO_JA_{solicitacao.status}',
            )

        now = datetime.now(timezone.utc)
        solicitacao.status = 'REJEITADA'
        solicitacao.analisada_em = now
        solicitacao.analisada_por = analisado_por
        solicitacao.motivo_rejeicao = dto.motivo_rejeicao.strip()

        await self.db.commit()
        await self.db.refresh(solicitacao)

        return SolicitacaoRejeicaoResponse(
            solicitacao_id=solicitacao.id,
            status=solicitacao.status,
            rejeitado_em=now,
            motivo_rejeicao=solicitacao.motivo_rejeicao,
        )

    @staticmethod
    def _ofuscar_email(email: str | None) -> str:
        if not email or '@' not in email:
            return '***@***.***'
        partes = email.split('@', 1)
        usuario, dominio = partes[0], partes[1]
        if len(usuario) <= 2:
            usuario_mascarado = usuario[0] + '***'
        else:
            usuario_mascarado = usuario[0] + '***' + usuario[-1]
        return f'{usuario_mascarado}@{dominio}'

    async def verificar_cpf_onboarding(
        self, dto: VerificarCpfOnboardingRequest
    ) -> VerificarCpfOnboardingResponse:
        import hashlib
        import re

        cpf_limpo = re.sub(r'\D', '', dto.cpf)
        if not cpf_limpo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='CPF_INVALIDO',
            )
        cpf_hash = hashlib.sha256(cpf_limpo.encode('utf-8')).hexdigest()

        # Buscar pessoa existente pelo cpf_hash
        stmt = select(Pessoa).where(Pessoa.cpf_hash == cpf_hash)
        pessoa = (await self.db.execute(stmt)).scalar_one_or_none()

        if not pessoa:
            return VerificarCpfOnboardingResponse(
                status='NOVO_CADASTRO',
                existe=False,
                email_ofuscado=None,
                mensagem='CPF não localizado no sistema. Prossiga com o preenchimento do formulário.',
                token_temporario=None,
            )

        # Mascarar o e-mail cadastrado
        email_ofuscado = self._ofuscar_email(pessoa.email)

        # Gerar Magic Link Token com validade de 15 minutos
        token = create_magic_link_token(
            {
                'tipo': 'MAGIC_LINK_ONBOARDING',
                'pessoa_id': str(pessoa.id),
                'condominio_id': str(dto.condominio_id),
            },
            expires_minutes=15,
        )

        return VerificarCpfOnboardingResponse(
            status='EXISTENTE_CONFIRMACAO_PENDENTE',
            existe=True,
            email_ofuscado=email_ofuscado,
            mensagem=(
                f'Detectamos um cadastro existente associado a este CPF. '
                f'Enviamos um link de validação de 15 minutos para {email_ofuscado}. '
                'Por favor, clique no link recebido para confirmar sua identidade.'
            ),
            token_temporario=token,
        )

    async def confirmar_magic_link(
        self, dto: ConfirmarMagicLinkRequest
    ) -> ConfirmarMagicLinkResponse:
        payload = decode_magic_link_token(dto.token)
        if not payload or payload.get('tipo') != 'MAGIC_LINK_ONBOARDING':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='TOKEN_INVALIDO_OU_EXPIRADO',
            )

        pessoa_id_str = payload.get('pessoa_id')
        if not pessoa_id_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='PAYLOAD_TOKEN_INVALIDO',
            )

        try:
            pessoa_id = uuid.UUID(pessoa_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='ID_PESSOA_INVALIDO',
            )

        pessoa = (
            await self.db.execute(select(Pessoa).where(Pessoa.id == pessoa_id))
        ).scalar_one_or_none()
        if not pessoa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='PESSOA_NAO_ENCONTRADA',
            )

        return ConfirmarMagicLinkResponse(
            sucesso=True,
            pessoa_id=pessoa.id,
            nome_completo=pessoa.nome_completo,
            email=pessoa.email,
            celular=pessoa.celular,
            mensagem='Identidade confirmada com sucesso. Seus dados foram carregados para conferência.',
        )

    async def revogar_vinculo(
        self, dto: RevogarVinculoRequest
    ) -> RevogarVinculoResponse:
        from app.modules.governanca.seguranca_auditoria.models import EventoAuditoria

        payload = decode_magic_link_token(dto.token)
        if not payload or payload.get('tipo') != 'REVOGACAO_VINCULO':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='TOKEN_REVOGACAO_INVALIDO_OU_EXPIRADO',
            )

        pessoa_id_str = payload.get('pessoa_id')
        condominio_id_str = payload.get('condominio_id')
        membro_id_str = payload.get('membro_id')

        now = datetime.now(timezone.utc)

        if membro_id_str:
            membro = (
                await self.db.execute(
                    select(MembroCondominio).where(
                        MembroCondominio.id == uuid.UUID(membro_id_str)
                    )
                )
            ).scalar_one_or_none()
            if membro:
                membro.status = 'INATIVO'

        if pessoa_id_str and condominio_id_str:
            ocupacoes = (
                await self.db.execute(
                    select(OcupacaoUnidade).where(
                        OcupacaoUnidade.pessoa_id == uuid.UUID(pessoa_id_str),
                        OcupacaoUnidade.condominio_id == uuid.UUID(condominio_id_str),
                        OcupacaoUnidade.status.in_(['ATIVO', 'ATIVA']),
                    )
                )
            ).scalars().all()
            for o in ocupacoes:
                o.status = 'INATIVO'
                o.fim_em = now

            auditoria = EventoAuditoria(
                condominio_id=uuid.UUID(condominio_id_str),
                pessoa_id=uuid.UUID(pessoa_id_str),
                acao='VINCULO_REVOGADO_PELO_TITULAR',
                entidade='membro_condominio',
                entidade_id=uuid.UUID(membro_id_str) if membro_id_str else None,
                dados_posteriores={
                    'revogado_em': now.isoformat(),
                    'motivo': 'Link preventivo de 15 minutos acionado pelo morador/titular',
                },
            )
            self.db.add(auditoria)

        await self.db.commit()

        return RevogarVinculoResponse(
            sucesso=True,
            mensagem='O vínculo com o condomínio foi revogado com sucesso a pedido do titular.',
            revogado_em=now,
        )
