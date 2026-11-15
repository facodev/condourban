import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import AreaComum
from .schemas import AreaComumCreate, AreaComumUpdate


class AreaComumService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_areas_comuns(
        self, condominio_id: uuid.UUID | None = None
    ) -> list[AreaComum]:
        query = select(AreaComum)
        if condominio_id:
            query = query.where(AreaComum.condominio_id == condominio_id)
        query = query.order_by(AreaComum.nome.asc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_area_comum(self, area_id: uuid.UUID) -> AreaComum:
        stmt = select(AreaComum).where(AreaComum.id == area_id)
        area = (await self.db.execute(stmt)).scalar_one_or_none()
        if not area:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='AREA_COMUM_NAO_ENCONTRADA',
            )
        return area

    async def create_area_comum(
        self, dto: AreaComumCreate, condominio_id: uuid.UUID | None = None
    ) -> AreaComum:
        c_id = dto.condominio_id or condominio_id
        if not c_id:
            from app.modules.condominio.branding.models import Condominio
            first_c = (await self.db.execute(select(Condominio))).scalars().first()
            c_id = first_c.id if first_c else uuid.uuid4()

        area = AreaComum(
            condominio_id=c_id,
            nome=dto.nome,
            descricao=dto.descricao,
            capacidade=dto.capacidade,
            requer_aprovacao=dto.requer_aprovacao,
            taxa_reserva=dto.taxa_reserva,
            valor_caucao=dto.valor_caucao,
            horario_abertura=dto.horario_abertura,
            horario_fechamento=dto.horario_fechamento,
            regras_dias=dto.regras_dias or {},
            ativo=dto.ativo,
        )
        self.db.add(area)
        await self.db.commit()
        await self.db.refresh(area)
        return area

    async def delete_area_comum(self, area_id: uuid.UUID) -> dict:
        area = await self.get_area_comum(area_id)
        try:
            from app.modules.reservas.agendamentos.models import ReservaAgendamento
            reservas = (
                await self.db.execute(
                    select(ReservaAgendamento).where(
                        ReservaAgendamento.area_comum_id == area_id,
                        ReservaAgendamento.status.in_(['CONFIRMADA', 'PENDENTE'])
                    )
                )
            ).scalars().all()
            if reservas:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'AREA_POSSUI_RESERVAS: O espaço "{area.nome}" possui {len(reservas)} reserva(s) ativa(s). Cancele as reservas antes de excluir.',
                )
        except (ImportError, Exception):
            pass

        await self.db.delete(area)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': f'Espaço "{area.nome}" excluído com sucesso.'}

    async def update_area_comum(
        self, area_id: uuid.UUID, dto: AreaComumUpdate
    ) -> AreaComum:
        area = await self.get_area_comum(area_id)
        if dto.nome is not None:
            area.nome = dto.nome
        if dto.descricao is not None:
            area.descricao = dto.descricao
        if dto.capacidade is not None:
            area.capacidade = dto.capacidade
        if dto.requer_aprovacao is not None:
            area.requer_aprovacao = dto.requer_aprovacao
        if dto.taxa_reserva is not None:
            area.taxa_reserva = dto.taxa_reserva
        if dto.valor_caucao is not None:
            area.valor_caucao = dto.valor_caucao
        if dto.horario_abertura is not None:
            area.horario_abertura = dto.horario_abertura
        if dto.horario_fechamento is not None:
            area.horario_fechamento = dto.horario_fechamento
        if dto.ativo is not None:
            area.ativo = dto.ativo
        if dto.regras_dias is not None:
            area.regras_dias = dto.regras_dias

        await self.db.commit()
        await self.db.refresh(area)
        return area

    async def delete_area_comum(self, area_id: uuid.UUID) -> dict:
        area = await self.get_area_comum(area_id)
        try:
            from app.modules.reservas.agendamentos.models import ReservaAgendamento
            reservas = (
                await self.db.execute(
                    select(ReservaAgendamento).where(
                        ReservaAgendamento.area_comum_id == area_id,
                        ReservaAgendamento.status.in_(['CONFIRMADA', 'PENDENTE'])
                    )
                )
            ).scalars().all()
            if reservas:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'AREA_POSSUI_RESERVAS: O espaço "{area.nome}" possui {len(reservas)} reserva(s) ativa(s). Cancele as reservas antes de excluir.',
                )
        except (ImportError, Exception):
            pass

        await self.db.delete(area)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': f'Espaço "{area.nome}" excluído com sucesso.'}


# Aliases de retrocompatibilidade
CommonAreaService = AreaComumService
