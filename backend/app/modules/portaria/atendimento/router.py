import uuid

from fastapi import APIRouter, status

from app.core.dependencies import ActiveCondominioDep, CurrentUserDep, SessionDep
from app.core.rbac import PAPEIS_OPERACAO_VISITANTES, exigir_papel
from .schemas import VisitanteCreate, VisitanteResponse
from .service import VisitanteService

router = APIRouter(
    prefix='/visitantes', tags=['Portaria - Atendimento e Visitantes']
)


def _uuid_or_none(value: str | uuid.UUID | None) -> uuid.UUID | None:
    if value is None:
        return None
    try:
        return uuid.UUID(str(value))
    except (ValueError, TypeError):
        return None


@router.get('', response_model=list[VisitanteResponse])
async def list_visitors(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> list[VisitanteResponse]:
    exigir_papel(
        current_user.get('papeis'),
        PAPEIS_OPERACAO_VISITANTES,
        'ACESSO_NEGADO_VISITANTES',
    )
    condo = condominio_id or _uuid_or_none(current_user.get('condominio_id'))
    service = VisitanteService(db)
    return await service.list_visitantes(condominio_id=condo)


@router.post(
    '', response_model=VisitanteResponse, status_code=status.HTTP_201_CREATED
)
async def create_visitor(
    dto: VisitanteCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> VisitanteResponse:
    exigir_papel(
        current_user.get('papeis'),
        PAPEIS_OPERACAO_VISITANTES,
        'ACESSO_NEGADO_VISITANTES',
    )
    condo = (
        dto.condominio_id
        or condominio_id
        or _uuid_or_none(current_user.get('condominio_id'))
    )
    service = VisitanteService(db)
    return await service.create_visitante(dto, condominio_id=condo)
