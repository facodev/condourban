import uuid
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.core.dependencies import ActiveCondominioDep, CurrentUserDep, SessionDep
from app.core.rbac import (
    assert_unidade_no_escopo,
    resolver_escopo_cadastro,
)
from .models import Pet, Veiculo
from .schemas import (
    PetCreate,
    PetResponse,
    VeiculoCreate,
    VeiculoResponse,
)
from .service import VeiculosPetsService

router = APIRouter(prefix='/veiculos-pets', tags=['Identidade - Veículos e Pets'])


@router.post(
    '/veiculos',
    response_model=VeiculoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def cadastrar_veiculo(
    dto: VeiculoCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> VeiculoResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    await assert_unidade_no_escopo(escopo, dto.unidade_id, escrita=True)
    service = VeiculosPetsService(db)
    return await service.cadastrar_veiculo(dto)


@router.get(
    '/veiculos',
    response_model=list[VeiculoResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_veiculos(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
    unidade_id: uuid.UUID | None = Query(None),
    placa: str | None = Query(None),
) -> list[VeiculoResponse]:
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = VeiculosPetsService(db)

    if not escopo['ver_todos']:
        if unidade_id:
            await assert_unidade_no_escopo(escopo, unidade_id)
            return await service.listar_veiculos(
                condominio_id=condominio_id,
                unidade_id=unidade_id,
                placa=placa,
            )
        return await service.listar_veiculos(
            condominio_id=condominio_id,
            unidade_ids=escopo['unidade_ids'],
            placa=placa,
        )

    return await service.listar_veiculos(
        condominio_id=condominio_id,
        unidade_id=unidade_id,
        placa=placa,
    )


@router.post(
    '/pets',
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def cadastrar_pet(
    dto: PetCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> PetResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    await assert_unidade_no_escopo(escopo, dto.unidade_id, escrita=True)
    service = VeiculosPetsService(db)
    return await service.cadastrar_pet(dto)


@router.get(
    '/pets',
    response_model=list[PetResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_pets(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
    unidade_id: uuid.UUID | None = Query(None),
) -> list[PetResponse]:
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = VeiculosPetsService(db)

    if not escopo['ver_todos']:
        if unidade_id:
            await assert_unidade_no_escopo(escopo, unidade_id)
            return await service.listar_pets(
                condominio_id=condominio_id,
                unidade_id=unidade_id,
            )
        return await service.listar_pets(
            condominio_id=condominio_id,
            unidade_ids=escopo['unidade_ids'],
        )

    return await service.listar_pets(
        condominio_id=condominio_id,
        unidade_id=unidade_id,
    )


@router.delete('/veiculos/{id}')
async def remover_veiculo(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    escopo = await resolver_escopo_cadastro(db, current_user)
    veiculo = (
        await db.execute(select(Veiculo).where(Veiculo.id == id))
    ).scalar_one_or_none()
    if not veiculo:
        raise HTTPException(status_code=404, detail='VEICULO_NAO_ENCONTRADO')
    await assert_unidade_no_escopo(escopo, veiculo.unidade_id, escrita=True)
    service = VeiculosPetsService(db)
    return await service.remover_veiculo(id)


@router.delete('/pets/{id}')
async def remover_pet(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    escopo = await resolver_escopo_cadastro(db, current_user)
    pet = (await db.execute(select(Pet).where(Pet.id == id))).scalar_one_or_none()
    if not pet:
        raise HTTPException(status_code=404, detail='PET_NAO_ENCONTRADO')
    await assert_unidade_no_escopo(escopo, pet.unidade_id, escrita=True)
    service = VeiculosPetsService(db)
    return await service.remover_pet(id)
