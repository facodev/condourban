import uuid
from fastapi import APIRouter, Query, status

from app.core.dependencies import ActiveCondominioDep, CurrentUserDep, SessionDep
from app.core.rbac import (
    negar_gestao_cadastro,
    resolver_escopo_cadastro,
)
from .schemas import (
    BlocoCreate,
    BlocoResponse,
    BlocoUpdate,
    UnidadeCreate,
    UnidadeResponse,
    UnidadeUpdate,
)
from .service import BlocosUnidadesService

router = APIRouter()


# =============================================================================
# Blocos / Torres
# =============================================================================


@router.get(
    '/blocos',
    response_model=list[BlocoResponse],
    tags=['Condomínio - Blocos & Unidades'],
)
@router.get(
    '/blocks',
    response_model=list[BlocoResponse],
    include_in_schema=False,
)
async def list_blocos(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> list[BlocoResponse]:
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = BlocosUnidadesService(db)
    if not escopo['ver_todos']:
        # Morador: só blocos das próprias unidades (para labels), sem catálogo completo
        return await service.list_blocos_por_unidades(
            escopo.get('unidade_ids') or [],
            condominio_id=condominio_id,
        )
    return await service.list_blocos(condominio_id=condominio_id)


@router.post(
    '/blocos',
    response_model=BlocoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Condomínio - Blocos & Unidades'],
)
@router.post(
    '/blocks',
    response_model=BlocoResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_bloco(
    dto: BlocoCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> BlocoResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    return await service.create_bloco(dto, condominio_id=condominio_id)


@router.patch(
    '/blocos/{id}',
    response_model=BlocoResponse,
    tags=['Condomínio - Blocos & Unidades'],
)
@router.put(
    '/blocos/{id}',
    response_model=BlocoResponse,
    include_in_schema=False,
)
@router.patch(
    '/blocks/{id}',
    response_model=BlocoResponse,
    include_in_schema=False,
)
async def update_bloco(
    id: uuid.UUID,
    dto: BlocoUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> BlocoResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    return await service.update_bloco(id, dto)


@router.delete(
    '/blocos/{id}',
    tags=['Condomínio - Blocos & Unidades'],
)
@router.delete(
    '/blocks/{id}',
    include_in_schema=False,
)
async def delete_bloco(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    return await service.delete_bloco(id)


# =============================================================================
# Unidades Autônomas
# =============================================================================


@router.get(
    '/unidades',
    response_model=list[UnidadeResponse],
    tags=['Condomínio - Blocos & Unidades'],
)
@router.get(
    '/units',
    response_model=list[UnidadeResponse],
    include_in_schema=False,
)
async def list_unidades(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
    bloco_id: uuid.UUID | None = Query(None),
) -> list[UnidadeResponse]:
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = BlocosUnidadesService(db)
    unidade_ids = None if escopo['ver_todos'] else (escopo.get('unidade_ids') or [])
    return await service.list_unidades(
        condominio_id=condominio_id,
        bloco_id=bloco_id,
        unidade_ids=unidade_ids,
    )


@router.post(
    '/unidades',
    response_model=UnidadeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Condomínio - Blocos & Unidades'],
)
@router.post(
    '/units',
    response_model=UnidadeResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_unidade(
    dto: UnidadeCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> UnidadeResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    return await service.create_unidade(dto, condominio_id=condominio_id)


@router.patch(
    '/unidades/{id}',
    response_model=UnidadeResponse,
    tags=['Condomínio - Blocos & Unidades'],
)
@router.put(
    '/unidades/{id}',
    response_model=UnidadeResponse,
    include_in_schema=False,
)
@router.patch(
    '/units/{id}',
    response_model=UnidadeResponse,
    include_in_schema=False,
)
async def update_unidade(
    id: uuid.UUID,
    dto: UnidadeUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> UnidadeResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    return await service.update_unidade(id, dto)


@router.delete(
    '/unidades/{id}',
    tags=['Condomínio - Blocos & Unidades'],
)
@router.delete(
    '/units/{id}',
    include_in_schema=False,
)
async def delete_unidade(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    return await service.delete_unidade(id)


@router.post(
    '/unidades/importar',
    status_code=status.HTTP_200_OK,
    tags=['Condomínio - Blocos & Unidades'],
)
async def importar_unidades(
    db: SessionDep,
    current_user: CurrentUserDep,
    payload: dict,
    condominio_id: uuid.UUID | None = Query(None),
) -> dict:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_ESTRUTURA')
    service = BlocosUnidadesService(db)
    conteudo_csv = payload.get('arquivo_csv', '')
    return await service.importar_unidades_csv(
        conteudo_csv, condominio_id=condominio_id
    )
