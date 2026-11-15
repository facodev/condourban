import random
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Encomenda
from .schemas import EncomendaCreate


class EncomendaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _gerar_pin() -> str:
        return f'{random.randint(0, 9999):04d}'

    async def list_encomendas(
        self,
        condominio_id: uuid.UUID | None = None,
        unidade_ids: list[uuid.UUID] | None = None,
    ) -> list[Encomenda]:
        query = select(Encomenda)
        if condominio_id:
            query = query.where(Encomenda.condominio_id == condominio_id)
        if unidade_ids is not None:
            if not unidade_ids:
                return []
            query = query.where(Encomenda.unidade_id.in_(unidade_ids))
        result = await self.db.execute(query.order_by(Encomenda.recebida_em.desc()))
        return list(result.scalars().all())

    async def create_encomenda(
        self,
        dto: EncomendaCreate,
        condominio_id: uuid.UUID | None = None,
        recebida_por: uuid.UUID | None = None,
    ) -> Encomenda:
        c_id = dto.condominio_id or condominio_id
        if not c_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='CONDOMINIO_OBRIGATORIO',
            )
        pin = self._gerar_pin()
        encomenda = Encomenda(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            destinatario_id=dto.destinatario_id,
            codigo_rastreio=dto.codigo_rastreio,
            transportadora=dto.transportadora,
            descricao=dto.descricao,
            status='RECEBIDA',
            local_armazenamento=dto.local_armazenamento,
            foto_url=dto.foto_url,
            observacao=dto.observacao,
            codigo_retirada=pin,
            recebida_por=recebida_por,
        )
        self.db.add(encomenda)
        await self.db.commit()
        await self.db.refresh(encomenda)
        return encomenda

    async def obter(self, encomenda_id: uuid.UUID) -> Encomenda | None:
        result = await self.db.execute(
            select(Encomenda).where(Encomenda.id == encomenda_id)
        )
        return result.scalar_one_or_none()

    async def dar_baixa(
        self,
        encomenda_id: uuid.UUID,
        codigo_retirada: str,
        retirada_por: uuid.UUID | None = None,
    ) -> Encomenda:
        encomenda = await self.obter(encomenda_id)
        if not encomenda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='ENCOMENDA_NAO_ENCONTRADA',
            )
        if encomenda.status == 'ENTREGUE':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='ENCOMENDA_JA_ENTREGUE',
            )
        if (encomenda.codigo_retirada or '') != str(codigo_retirada).strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='PIN_INVALIDO',
            )
        encomenda.status = 'ENTREGUE'
        encomenda.retirada_em = datetime.now(timezone.utc)
        encomenda.retirada_por = retirada_por
        await self.db.commit()
        await self.db.refresh(encomenda)
        return encomenda


# Aliases de retrocompatibilidade
DeliveryService = EncomendaService
