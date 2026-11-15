import uuid

from fastapi import APIRouter, status

from app.core.dependencies import ActiveCondominioDep, CurrentUserDep, SessionDep
from app.core.rbac import (
    PAPEIS_OPERACAO_ENCOMENDAS,
    exigir_papel,
    pode_ver_todos_cadastros,
    resolver_escopo_cadastro,
)
from .schemas import BaixaEncomendaRequest, EncomendaCreate, EncomendaResponse
from .service import EncomendaService

router = APIRouter(prefix='/encomendas', tags=['Portaria - Encomendas'])


def _uuid_or_none(value: str | uuid.UUID | None) -> uuid.UUID | None:
    if value is None:
        return None
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError):
        return None


@router.get('', response_model=list[EncomendaResponse])
async def list_deliveries(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> list[EncomendaResponse]:
    condo = condominio_id or _uuid_or_none(current_user.get('condominio_id'))
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = EncomendaService(db)
    if pode_ver_todos_cadastros(current_user.get('papeis')):
        return await service.list_encomendas(condominio_id=condo)
    unidade_ids = list(escopo.get('unidade_ids') or [])
    if not unidade_ids:
        for raw in current_user.get('unidade_ids') or []:
            uid = _uuid_or_none(raw)
            if uid:
                unidade_ids.append(uid)
    return await service.list_encomendas(
        condominio_id=condo,
        unidade_ids=unidade_ids,
    )


@router.post(
    '', response_model=EncomendaResponse, status_code=status.HTTP_201_CREATED
)
async def create_delivery(
    dto: EncomendaCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> EncomendaResponse:
    exigir_papel(
        current_user.get('papeis'),
        PAPEIS_OPERACAO_ENCOMENDAS,
        'ACESSO_NEGADO_ENCOMENDAS',
    )
    condo = (
        dto.condominio_id
        or condominio_id
        or _uuid_or_none(current_user.get('condominio_id'))
    )
    service = EncomendaService(db)
    return await service.create_encomenda(
        dto,
        condominio_id=condo,
        recebida_por=_uuid_or_none(current_user.get('pessoa_id')),
    )


@router.post('/{encomenda_id}/baixa', response_model=EncomendaResponse)
async def baixar_encomenda(
    encomenda_id: uuid.UUID,
    dto: BaixaEncomendaRequest,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> EncomendaResponse:
    exigir_papel(
        current_user.get('papeis'),
        PAPEIS_OPERACAO_ENCOMENDAS,
        'ACESSO_NEGADO_ENCOMENDAS',
    )
    service = EncomendaService(db)
    return await service.dar_baixa(
        encomenda_id,
        dto.codigo_retirada,
        retirada_por=_uuid_or_none(current_user.get('pessoa_id')),
    )
