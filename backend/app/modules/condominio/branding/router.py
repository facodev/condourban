import uuid
from fastapi import APIRouter, status

from app.core.dependencies import ActiveCondominioDep, SessionDep
from .schemas import (
    CondominioInfoResponse,
    CondominioInfoUpdate,
    ConfiguracaoCondominioUpdate,
)
from .service import BrandingService

router = APIRouter()


@router.get(
    '/info',
    response_model=CondominioInfoResponse,
    tags=['Condomínio - Institucional & Branding'],
)
async def obter_condominio_info(
    db: SessionDep,
    condominio_id: ActiveCondominioDep,
) -> CondominioInfoResponse:
    service = BrandingService(db)
    condominio = await service.get_or_create_condominio(condominio_id)
    return CondominioInfoResponse.model_validate(condominio)


@router.put(
    '/info',
    response_model=CondominioInfoResponse,
    tags=['Condomínio - Institucional & Branding'],
)
async def atualizar_condominio_info(
    dto: CondominioInfoUpdate,
    db: SessionDep,
    condominio_id: ActiveCondominioDep,
) -> CondominioInfoResponse:
    service = BrandingService(db)
    condominio = await service.update_condominio_info(condominio_id, dto)
    return CondominioInfoResponse.model_validate(condominio)


@router.get(
    '/configuracoes',
    response_model=dict,
    tags=['Condomínio - Institucional & Branding'],
)
async def obter_configuracoes(
    db: SessionDep,
    condominio_id: ActiveCondominioDep,
) -> dict:
    service = BrandingService(db)
    return await service.get_configuracoes(condominio_id)


@router.patch(
    '/configuracoes',
    response_model=dict,
    tags=['Condomínio - Institucional & Branding'],
)
async def atualizar_configuracoes(
    dto: ConfiguracaoCondominioUpdate,
    db: SessionDep,
    condominio_id: ActiveCondominioDep,
) -> dict:
    service = BrandingService(db)
    return await service.update_configuracoes(condominio_id, dto)


@router.get(
    '/todos',
    response_model=list[CondominioInfoResponse],
    tags=['Condomínio - Multi-tenant Admin'],
)
@router.get(
    '/condominios',
    response_model=list[CondominioInfoResponse],
    include_in_schema=False,
)
async def list_condominios(
    db: SessionDep,
) -> list[CondominioInfoResponse]:
    service = BrandingService(db)
    condos = await service.list_condominios()
    return [CondominioInfoResponse.model_validate(c) for c in condos]


@router.post(
    '/novo',
    response_model=CondominioInfoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Condomínio - Multi-tenant Admin'],
)
@router.post(
    '/condominios',
    response_model=CondominioInfoResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_condominio(
    dto: CondominioInfoUpdate,
    db: SessionDep,
) -> CondominioInfoResponse:
    service = BrandingService(db)
    condo = await service.create_condominio(dto)
    return CondominioInfoResponse.model_validate(condo)


@router.delete(
    '/condominios/{id}',
    tags=['Condomínio - Multi-tenant Admin'],
)
async def delete_condominio(
    id: uuid.UUID,
    db: SessionDep,
) -> dict:
    service = BrandingService(db)
    return await service.delete_condominio(id)
