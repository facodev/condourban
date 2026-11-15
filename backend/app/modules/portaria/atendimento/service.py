import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identidade_cadastro.pessoas.models import Pessoa

from .models import Visitante
from .schemas import VisitanteCreate


class VisitanteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_visitantes(
        self, condominio_id: uuid.UUID | None = None
    ) -> list[Visitante]:
        query = select(Visitante)
        if condominio_id:
            query = query.where(Visitante.condominio_id == condominio_id)
        result = await self.db.execute(query.order_by(Visitante.criado_em.desc()))
        visitantes = list(result.scalars().all())
        for v in visitantes:
            if v.pessoa_id:
                pessoa = (
                    await self.db.execute(
                        select(Pessoa).where(Pessoa.id == v.pessoa_id)
                    )
                ).scalar_one_or_none()
                if pessoa:
                    v.nome_completo = pessoa.nome_completo
                    v.documento = pessoa.cpf
        return visitantes

    async def create_visitante(
        self,
        dto: VisitanteCreate,
        condominio_id: uuid.UUID | None = None,
    ) -> Visitante:
        c_id = dto.condominio_id or condominio_id
        if not c_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='CONDOMINIO_OBRIGATORIO',
            )

        pessoa_id = dto.pessoa_id
        if not pessoa_id:
            nome = (dto.nome_completo or '').strip() or 'Visitante'
            pessoa = Pessoa(
                id=uuid.uuid4(),
                inquilino_id=uuid.uuid4(),
                nome_completo=nome,
                status='ATIVO',
            )
            if dto.documento:
                import base64

                pessoa.cpf_criptografado = base64.b64encode(
                    dto.documento.encode('utf-8')
                ).decode('utf-8')
            self.db.add(pessoa)
            await self.db.flush()
            pessoa_id = pessoa.id

        visitante = Visitante(
            condominio_id=c_id,
            pessoa_id=pessoa_id,
            unidade_id=dto.unidade_id,
            responsavel_id=dto.responsavel_id,
            observacao=dto.observacao,
            status=dto.status or 'AUTORIZADO',
        )
        self.db.add(visitante)
        await self.db.commit()
        await self.db.refresh(visitante)

        visitante.nome_completo = dto.nome_completo
        visitante.documento = dto.documento
        return visitante


# Aliases de retrocompatibilidade
VisitorService = VisitanteService
