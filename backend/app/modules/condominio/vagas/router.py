import uuid
from fastapi import APIRouter, Query, status

from app.core.dependencies import ActiveCondominioDep, SessionDep
from .schemas import (
    VagaGaragemCreate,
    VagaGaragemResponse,
    VagaGaragemUpdate,
)
from .service import VagasService

router = APIRouter()


@router.get(
    '/vagas',
    response_model=list[VagaGaragemResponse],
    tags=['Condomínio - Vagas de Garagem'],
)
async def list_vagas(
    db: SessionDep,
    condominio_id: ActiveCondominioDep = None,
    unidade_id: uuid.UUID | None = Query(None),
) -> list[VagaGaragemResponse]:
    service = VagasService(db)
    return await service.list_vagas(
        condominio_id=condominio_id, unidade_id=unidade_id
    )


@router.post(
    '/vagas',
    response_model=VagaGaragemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Condomínio - Vagas de Garagem'],
)
async def create_vaga(
    dto: VagaGaragemCreate,
    db: SessionDep,
    condominio_id: ActiveCondominioDep = None,
) -> VagaGaragemResponse:
    service = VagasService(db)
    return await service.create_vaga(dto, condominio_id=condominio_id)


@router.patch(
    '/vagas/{id}',
    response_model=VagaGaragemResponse,
    tags=['Condomínio - Vagas de Garagem'],
)
async def update_vaga(
    id: uuid.UUID,
    dto: VagaGaragemUpdate,
    db: SessionDep,
) -> VagaGaragemResponse:
    service = VagasService(db)
    return await service.update_vaga(id, dto)


@router.delete(
    '/vagas/{id}',
    tags=['Condomínio - Vagas de Garagem'],
)
async def delete_vaga(
    id: uuid.UUID,
    db: SessionDep,
) -> dict:
    service = VagasService(db)
    return await service.delete_vaga(id)

