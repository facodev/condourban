import uuid
from fastapi import APIRouter, status, Query

from app.core.dependencies import SessionDep
from .schemas import ReservaCreate, ReservaResponse
from .service import ReservaService

router = APIRouter(tags=['Reservas - Agendamentos'])


@router.get('/reservas', response_model=list[ReservaResponse])
async def list_reservations(
    db: SessionDep,
    condominio_id: uuid.UUID | None = Query(None)
) -> list[ReservaResponse]:
    service = ReservaService(db)
    return await service.list_reservas(condominio_id=condominio_id)


@router.post(
    '/reservas', response_model=ReservaResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    dto: ReservaCreate,
    db: SessionDep,
    condominio_id: uuid.UUID | None = Query(None)
) -> ReservaResponse:
    service = ReservaService(db)
    return await service.create_reserva(dto, condominio_id=condominio_id)
