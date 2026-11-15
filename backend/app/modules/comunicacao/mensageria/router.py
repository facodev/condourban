import uuid
from fastapi import APIRouter, HTTPException, Query, status

from app.core.dependencies import OptionalCurrentUserDep, SessionDep
from .schemas import (
    ComunicadoCreate,
    ComunicadoResponse,
    ConfirmarLeituraResponse,
)
from .service import ComunicadoService

router = APIRouter(
    prefix='/comunicados', tags=['Comunicação - Mensageria']
)


@router.get('', response_model=list[ComunicadoResponse])
async def list_notices(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    pessoa_id: uuid.UUID | None = Query(None),
) -> list[ComunicadoResponse]:
    target_condo_id = condominio_id
    target_pessoa_id = pessoa_id
    if current_user:
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if not target_pessoa_id and current_user.get('user_id'):
            target_pessoa_id = uuid.UUID(current_user['user_id'])

    service = ComunicadoService(db)
    items = await service.list_comunicados(
        condominio_id=target_condo_id,
        pessoa_id=target_pessoa_id,
    )
    return [ComunicadoResponse(**item) for item in items]


@router.get('/urgentes-pendentes', response_model=list[ComunicadoResponse])
async def list_urgentes_pendentes(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    pessoa_id: uuid.UUID | None = Query(None),
) -> list[ComunicadoResponse]:
    target_condo_id = condominio_id
    target_pessoa_id = pessoa_id
    if current_user:
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if not target_pessoa_id and current_user.get('user_id'):
            target_pessoa_id = uuid.UUID(current_user['user_id'])

    if not target_pessoa_id:
        return []

    service = ComunicadoService(db)
    items = await service.verificar_urgentes_pendentes(
        condominio_id=target_condo_id,
        pessoa_id=target_pessoa_id,
    )
    return [ComunicadoResponse(**item) for item in items]


@router.post(
    '', response_model=ComunicadoResponse, status_code=status.HTTP_201_CREATED
)
async def create_notice(
    dto: ComunicadoCreate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    autor_id: uuid.UUID | None = Query(None),
) -> ComunicadoResponse:
    if current_user:
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        is_gestao = any(p in papeis for p in ('sindico', 'administradora', 'subsindico', 'conselho', 'admin'))
        if 'morador' in papeis and not is_gestao:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='PERMISSAO_NEGADA',
            )

    target_condo_id = condominio_id
    target_autor_id = autor_id or dto.autor_id
    if current_user:
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if not target_autor_id and current_user.get('user_id'):
            target_autor_id = uuid.UUID(current_user['user_id'])

    service = ComunicadoService(db)
    return await service.create_comunicado(
        dto, condominio_id=target_condo_id, autor_id=target_autor_id
    )


@router.post(
    '/{id}/confirmar-leitura',
    response_model=ConfirmarLeituraResponse,
    status_code=status.HTTP_200_OK,
)
async def confirmar_leitura(
    id: uuid.UUID,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    pessoa_id: uuid.UUID | None = Query(None),
) -> ConfirmarLeituraResponse:
    target_pessoa_id = pessoa_id
    target_condo_id = None
    if current_user:
        if not target_pessoa_id and current_user.get('user_id'):
            target_pessoa_id = uuid.UUID(current_user['user_id'])
        if current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])

    if not target_pessoa_id:
        target_pessoa_id = uuid.uuid4()

    service = ComunicadoService(db)
    result = await service.confirmar_leitura(
        comunicado_id=id,
        pessoa_id=target_pessoa_id,
        condominio_id=target_condo_id,
    )
    return ConfirmarLeituraResponse(**result)

