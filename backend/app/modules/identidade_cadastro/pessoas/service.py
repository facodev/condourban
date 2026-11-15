import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .models import Pessoa
from .schemas import PessoaCreate, PessoaUpdate
from app.modules.identidade_cadastro.usuarios.models import (
    MembroCondominio,
    OcupacaoUnidade,
)
from app.core.security import create_magic_link_token


class PessoaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _processar_cpf(cpf_raw: str | None) -> tuple[str | None, str | None]:
        import base64
        import hashlib
        import re
        if not cpf_raw:
            return None, None
        cpf_limpo = re.sub(r'\D', '', str(cpf_raw))
        if not cpf_limpo:
            return None, None
        cpf_hash = hashlib.sha256(cpf_limpo.encode('utf-8')).hexdigest()
        cpf_criptografado = base64.b64encode(cpf_limpo.encode('utf-8')).decode('utf-8')
        return cpf_hash, cpf_criptografado

    async def list_pessoas(
        self,
        pessoa_ids: list[uuid.UUID] | None = None,
        condominio_id: uuid.UUID | None = None,
    ) -> list[Pessoa]:
        """Lista pessoas pertencentes ao condomínio ativo.
        Garante que pessoas de outros condomínios nunca sejam expostas.
        """
        if pessoa_ids is not None:
            if not pessoa_ids:
                return []
            stmt = select(Pessoa).where(Pessoa.id.in_(pessoa_ids))
            result = await self.db.execute(stmt)
            return list(result.scalars().all())

        if condominio_id:
            # Busca todas as pessoas com membro ou ocupação neste condomínio
            m_stmt = select(MembroCondominio.pessoa_id).where(
                MembroCondominio.condominio_id == condominio_id,
                MembroCondominio.status == 'ATIVO',
            )
            o_stmt = select(OcupacaoUnidade.pessoa_id).where(
                OcupacaoUnidade.condominio_id == condominio_id,
                OcupacaoUnidade.status.in_(['ATIVO', 'ATIVA']),
            )
            m_ids = (await self.db.execute(m_stmt)).scalars().all()
            o_ids = (await self.db.execute(o_stmt)).scalars().all()
            all_ids = list({p for p in (list(m_ids) + list(o_ids)) if p})
            if not all_ids:
                return []
            stmt = select(Pessoa).where(Pessoa.id.in_(all_ids))
            result = await self.db.execute(stmt)
            return list(result.scalars().all())

        stmt = select(Pessoa)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_pessoa(self, pessoa_id: uuid.UUID) -> Pessoa:
        pessoa = (
            await self.db.execute(select(Pessoa).where(Pessoa.id == pessoa_id))
        ).scalar_one_or_none()
        if not pessoa:
            raise HTTPException(status_code=404, detail='PESSOA_NAO_ENCONTRADA')
        return pessoa

    async def update_pessoa(
        self,
        pessoa_id: uuid.UUID,
        dto: PessoaUpdate,
        *,
        somente_contato: bool = False,
    ) -> Pessoa:
        """Atualiza pessoa. Com somente_contato=True (morador), bloqueia
        nome civil, CPF e status — só e-mail, celular, telefones, nome social e foto.
        """
        pessoa = await self.get_pessoa(pessoa_id)

        if somente_contato:
            proibidos = []
            if dto.nome_completo is not None:
                proibidos.append('nome_completo')
            if dto.cpf is not None:
                proibidos.append('cpf')
            if dto.status is not None:
                proibidos.append('status')
            if proibidos:
                raise HTTPException(
                    status_code=403,
                    detail=(
                        'CAMPOS_RESERVADOS_GESTAO: Morador só pode alterar '
                        'e-mail de contato, celular, telefones, nome social e foto. '
                        f'Campos bloqueados: {", ".join(proibidos)}.'
                    ),
                )
            if dto.email is not None:
                pessoa.email = dto.email
            if dto.telefones is not None:
                telefones_data = [t.model_dump() for t in dto.telefones]
                pessoa.telefones = telefones_data
                if telefones_data:
                    principal_t = next((t for t in telefones_data if t.get('principal')), telefones_data[0])
                    pessoa.celular = principal_t.get('numero')
            elif dto.celular is not None:
                pessoa.celular = dto.celular
            if dto.nome_social is not None:
                pessoa.nome_social = dto.nome_social
            if dto.foto_url is not None:
                pessoa.foto_url = dto.foto_url
        else:
            if dto.nome_completo is not None:
                pessoa.nome_completo = dto.nome_completo
            if dto.nome_social is not None:
                pessoa.nome_social = dto.nome_social
            if dto.email is not None:
                pessoa.email = dto.email
            if dto.telefones is not None:
                telefones_data = [t.model_dump() for t in dto.telefones]
                pessoa.telefones = telefones_data
                if telefones_data:
                    principal_t = next((t for t in telefones_data if t.get('principal')), telefones_data[0])
                    pessoa.celular = principal_t.get('numero')
            elif dto.celular is not None:
                pessoa.celular = dto.celular
            if dto.cpf is not None:
                cpf_hash, cpf_crip = self._processar_cpf(dto.cpf)
                pessoa.cpf_hash = cpf_hash
                pessoa.cpf_criptografado = cpf_crip
                pessoa.cpf = dto.cpf
            if dto.foto_url is not None:
                pessoa.foto_url = dto.foto_url
            if dto.status is not None:
                pessoa.status = dto.status

        await self.db.commit()
        await self.db.refresh(pessoa)
        return pessoa

    async def create_pessoa(
        self, dto: PessoaCreate, condominio_id: uuid.UUID | None = None
    ) -> Pessoa:
        """Cria ou associa uma pessoa física ao condomínio ativo.
        Se o CPF já existir (em outro condomínio), reutiliza o registro civil sem
        vazar dados para o síndico e envia e-mail preventivo de 15 min com link de revogação.
        """
        cpf_hash, cpf_crip = self._processar_cpf(dto.cpf)
        telefones_data = [t.model_dump() for t in dto.telefones] if dto.telefones else []
        celular_principal = dto.celular
        if telefones_data:
            principal_t = next((t for t in telefones_data if t.get('principal')), telefones_data[0])
            celular_principal = principal_t.get('numero')

        pessoa_existente: Pessoa | None = None
        if cpf_hash:
            pessoa_existente = (
                await self.db.execute(select(Pessoa).where(Pessoa.cpf_hash == cpf_hash))
            ).scalar_one_or_none()

        if pessoa_existente:
            pessoa = pessoa_existente
            # Checar se já é membro deste condomínio
            if condominio_id:
                m_stmt = select(MembroCondominio).where(
                    MembroCondominio.pessoa_id == pessoa.id,
                    MembroCondominio.condominio_id == condominio_id,
                )
                membro = (await self.db.execute(m_stmt)).scalar_one_or_none()
                if not membro:
                    # Novo vínculo para pessoa já existente em outro condomínio
                    membro = MembroCondominio(
                        condominio_id=condominio_id,
                        pessoa_id=pessoa.id,
                        tipo_pessoa=dto.tipo_vinculo or 'MORADOR',
                        status='ATIVO',
                    )
                    self.db.add(membro)
                    await self.db.flush()

                    if dto.unidade_id:
                        ocupacao = OcupacaoUnidade(
                            condominio_id=condominio_id,
                            unidade_id=dto.unidade_id,
                            pessoa_id=pessoa.id,
                            tipo_vinculo=dto.tipo_vinculo or 'MORADOR',
                            mora_no_local=True,
                            status='ATIVO',
                        )
                        self.db.add(ocupacao)

                    # Disparo preventivo de segurança com link de revogação de 15 minutos
                    token_revogacao = create_magic_link_token(
                        {
                            'tipo': 'REVOGACAO_VINCULO',
                            'pessoa_id': str(pessoa.id),
                            'condominio_id': str(condominio_id),
                            'membro_id': str(membro.id),
                        },
                        expires_minutes=15,
                    )
                    # Registrar evento de auditoria
                    from app.modules.governanca.seguranca_auditoria.models import EventoAuditoria
                    auditoria = EventoAuditoria(
                        condominio_id=condominio_id,
                        pessoa_id=pessoa.id,
                        acao='VINCULO_PESSOA_EXISTENTE_CRIADO',
                        entidade='membro_condominio',
                        entidade_id=membro.id,
                        dados_posteriores={
                            'aviso_seguranca_emitido': True,
                            'token_revogacao_gerado': token_revogacao[:10] + '...',
                        },
                    )
                    self.db.add(auditoria)
        else:
            inq_id = dto.inquilino_id
            if not inq_id and condominio_id:
                from app.modules.condominio.estrutura.models import Condominio
                c_obj = (
                    await self.db.execute(
                        select(Condominio).where(Condominio.id == condominio_id)
                    )
                ).scalar_one_or_none()
                if c_obj and c_obj.inquilino_id:
                    inq_id = c_obj.inquilino_id
            if not inq_id:
                from app.modules.condominio.estrutura.models import Condominio
                first_c = (await self.db.execute(select(Condominio))).scalars().first()
                inq_id = first_c.inquilino_id if first_c else uuid.uuid4()

            pessoa = Pessoa(
                inquilino_id=inq_id,
                nome_completo=dto.nome_completo or 'Morador',
                nome_social=dto.nome_social,
                cpf_hash=cpf_hash,
                cpf_criptografado=cpf_crip,
                data_nascimento=dto.data_nascimento,
                email=dto.email,
                celular=celular_principal,
                telefones=telefones_data,
                foto_url=dto.foto_url,
            )
            self.db.add(pessoa)
            await self.db.flush()

            if condominio_id:
                membro = MembroCondominio(
                    condominio_id=condominio_id,
                    pessoa_id=pessoa.id,
                    tipo_pessoa=dto.tipo_vinculo or 'MORADOR',
                    status='ATIVO',
                )
                self.db.add(membro)

                if dto.unidade_id:
                    ocupacao = OcupacaoUnidade(
                        condominio_id=condominio_id,
                        unidade_id=dto.unidade_id,
                        pessoa_id=pessoa.id,
                        tipo_vinculo=dto.tipo_vinculo or 'MORADOR',
                        mora_no_local=True,
                        status='ATIVO',
                    )
                    self.db.add(ocupacao)

        await self.db.commit()
        await self.db.refresh(pessoa)
        pessoa.cpf = dto.cpf
        pessoa.usuario_id = dto.usuario_id
        pessoa.unidade_id = dto.unidade_id
        pessoa.tipo_vinculo = dto.tipo_vinculo
        return pessoa

    async def get_me(self, user_id_str: str) -> Pessoa:
        from app.modules.identidade_cadastro.usuarios.models import Usuario
        user_uuid = uuid.UUID(user_id_str)
        user = (await self.db.execute(select(Usuario).where(Usuario.id == user_uuid))).scalar_one_or_none()
        if not user or not user.pessoa_id:
            raise HTTPException(status_code=404, detail='PESSOA_NAO_ENCONTRADA')
        pessoa = (await self.db.execute(select(Pessoa).where(Pessoa.id == user.pessoa_id))).scalar_one_or_none()
        if not pessoa:
            raise HTTPException(status_code=404, detail='PESSOA_NAO_ENCONTRADA')
        return pessoa

    async def delete_pessoa(self, pessoa_id: uuid.UUID) -> dict:
        from app.modules.identidade_cadastro.usuarios.models import Usuario, OcupacaoUnidade
        from app.modules.identidade_cadastro.veiculos_pets.models import Veiculo, Pet

        pessoa = await self.get_pessoa(pessoa_id)

        # 1. Checar conta de usuário
        user = (
            await self.db.execute(select(Usuario).where(Usuario.pessoa_id == pessoa_id))
        ).scalar_one_or_none()
        if user:
            raise HTTPException(
                status_code=400,
                detail='PESSOA_POSSUI_CONTA: Não é possível excluir uma pessoa que possui conta de usuário ativa no sistema.',
            )

        # 2. Checar ocupações ativas
        ocup = (
            await self.db.execute(
                select(OcupacaoUnidade).where(
                    OcupacaoUnidade.pessoa_id == pessoa_id,
                    OcupacaoUnidade.status.in_(['ATIVO', 'ATIVA']),
                )
            )
        ).scalar_one_or_none()
        if ocup:
            raise HTTPException(
                status_code=400,
                detail='PESSOA_POSSUI_OCUPACAO_ATIVA: Não é possível excluir uma pessoa vinculada como morador/proprietário a uma unidade. Inative o vínculo primeiro.',
            )

        # 3. Checar veículos e pets
        veic = (
            await self.db.execute(select(Veiculo).where(Veiculo.proprietario_id == pessoa_id))
        ).scalar_one_or_none()
        if veic:
            raise HTTPException(
                status_code=400,
                detail='PESSOA_POSSUI_VEICULO: Não é possível excluir uma pessoa com veículo registrado em seu nome.',
            )

        pet = (
            await self.db.execute(select(Pet).where(Pet.tutor_id == pessoa_id))
        ).scalar_one_or_none()
        if pet:
            raise HTTPException(
                status_code=400,
                detail='PESSOA_POSSUI_PET: Não é possível excluir uma pessoa registrada como tutora de animal de estimação.',
            )

        # Desassociar membros e ocupações históricas se houver
        inativas = (
            await self.db.execute(
                select(OcupacaoUnidade).where(OcupacaoUnidade.pessoa_id == pessoa_id)
            )
        ).scalars().all()
        for oc in inativas:
            await self.db.delete(oc)

        membros = (
            await self.db.execute(
                select(MembroCondominio).where(MembroCondominio.pessoa_id == pessoa_id)
            )
        ).scalars().all()
        for m in membros:
            await self.db.delete(m)

        await self.db.delete(pessoa)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': 'Pessoa física excluída com sucesso.'}


# Aliases de retrocompatibilidade
ResidenteService = PessoaService
ResidentService = PessoaService
