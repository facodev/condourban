import uuid
from fastapi import APIRouter, Query, status

from app.core.dependencies import OptionalCurrentUserDep, SessionDep
from .schemas import (
    MensagemFaleConoscoCreate,
    MensagemFaleConoscoResponse,
)
from .service import FaleConoscoService

router = APIRouter(prefix='/fale-conosco', tags=['Comunicação - Fale Conosco'])


@router.get('', response_model=list[MensagemFaleConoscoResponse])
async def list_mensagens_fale_conosco(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    unidade_id: uuid.UUID | None = Query(None),
    remetente_id: uuid.UUID | None = Query(None),
) -> list[MensagemFaleConoscoResponse]:
    target_condo_id = condominio_id
    target_remetente_id = remetente_id
    is_admin = False

    if current_user:
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        is_admin = any(p in papeis for p in ('sindico', 'administradora', 'subsindico', 'admin'))
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if not target_remetente_id and current_user.get('user_id'):
            target_remetente_id = uuid.UUID(current_user['user_id'])

    service = FaleConoscoService(db)
    return await service.list_mensagens(
        condominio_id=target_condo_id,
        unidade_id=unidade_id,
        remetente_id=target_remetente_id,
        is_admin=is_admin,
    )


@router.post(
    '',
    response_model=MensagemFaleConoscoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_mensagem_fale_conosco(
    dto: MensagemFaleConoscoCreate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    remetente_id: uuid.UUID | None = Query(None),
) -> MensagemFaleConoscoResponse:
    target_condo_id = condominio_id
    target_remetente_id = remetente_id or dto.remetente_id
    if current_user:
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if not target_remetente_id and current_user.get('user_id'):
            target_remetente_id = uuid.UUID(current_user['user_id'])

    service = FaleConoscoService(db)
    return await service.create_mensagem(
        dto, condominio_id=target_condo_id, remetente_id=target_remetente_id
    )
