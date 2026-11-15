from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from .models import Reserva
from .schemas import ReservaCreate


class ReservaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_reservas(self, condominio_id: uuid.UUID | None = None) -> list[Reserva]:
        query = select(Reserva)
        if condominio_id:
            query = query.where(Reserva.condominio_id == condominio_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_reserva(self, dto: ReservaCreate, condominio_id: uuid.UUID | None = None) -> Reserva:
        c_id = condominio_id or uuid.uuid4()
        s_id = dto.solicitante_id or dto.usuario_id or uuid.uuid4()
        reserva = Reserva(
            condominio_id=c_id,
            area_comum_id=dto.area_comum_id,
            unidade_id=dto.unidade_id,
            solicitante_id=s_id,
            inicio_em=dto.inicio_em,
            fim_em=dto.fim_em,
            valor=dto.valor,
            termo_aceito=dto.termo_aceito,
            status=dto.status,
            observacao=dto.observacao,
        )
        self.db.add(reserva)
        await self.db.commit()
        await self.db.refresh(reserva)
        return reserva


# Aliases de retrocompatibilidade
ReservationService = ReservaService
