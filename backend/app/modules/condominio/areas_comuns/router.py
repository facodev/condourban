import uuid
from fastapi import APIRouter, Query, status

from app.core.dependencies import ActiveCondominioDep, SessionDep
from .schemas import (
    AreaComumCreate,
    AreaComumResponse,
    AreaComumUpdate,
)
from .service import AreaComumService

router = APIRouter(prefix='/areas-comuns', tags=['Condomínio - Áreas Comuns'])


@router.get('', response_model=list[AreaComumResponse])
async def list_common_areas(
    db: SessionDep,
    condominio_id: ActiveCondominioDep = None,
) -> list[AreaComumResponse]:
    service = AreaComumService(db)
    return await service.list_areas_comuns(condominio_id=condominio_id)


@router.post(
    '', response_model=AreaComumResponse, status_code=status.HTTP_201_CREATED
)
async def create_common_area(
    dto: AreaComumCreate,
    db: SessionDep,
    condominio_id: ActiveCondominioDep = None,
) -> AreaComumResponse:
    service = AreaComumService(db)
    return await service.create_area_comum(dto, condominio_id=condominio_id)


@router.get('/{id}', response_model=AreaComumResponse)
async def get_common_area(
    id: uuid.UUID,
    db: SessionDep,
) -> AreaComumResponse:
    service = AreaComumService(db)
    return await service.get_area_comum(id)


@router.patch('/{id}', response_model=AreaComumResponse)
@router.put('/{id}', response_model=AreaComumResponse, include_in_schema=False)
async def update_common_area(
    id: uuid.UUID,
    dto: AreaComumUpdate,
    db: SessionDep,
) -> AreaComumResponse:
    service = AreaComumService(db)
    return await service.update_area_comum(id, dto)


@router.delete('/{id}')
async def delete_common_area(
    id: uuid.UUID,
    db: SessionDep,
) -> dict:
    service = AreaComumService(db)
    return await service.delete_area_comum(id)
