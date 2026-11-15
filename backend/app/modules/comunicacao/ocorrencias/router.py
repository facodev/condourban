import uuid
from fastapi import APIRouter, Query, status

from app.core.dependencies import OptionalCurrentUserDep, SessionDep
from .schemas import (
    HistoricoOcorrenciaCreate,
    HistoricoOcorrenciaResponse,
    OcorrenciaCreate,
    OcorrenciaResponse,
    OcorrenciaStatusUpdate,
)
from .service import OcorrenciaService

router = APIRouter(prefix='/ocorrencias', tags=['Comunicação - Ocorrências'])


@router.get('', response_model=list[OcorrenciaResponse])
async def list_occurrences(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
) -> list[OcorrenciaResponse]:
    target_condo_id = condominio_id
    current_user_id = None
    is_admin = False

    if current_user:
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if current_user.get('user_id'):
            current_user_id = uuid.UUID(current_user['user_id'])
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        is_admin = any(p in papeis for p in ('sindico', 'administradora', 'subsindico', 'admin'))

    service = OcorrenciaService(db)
    items = await service.list_ocorrencias(
        condominio_id=target_condo_id,
        current_user_id=current_user_id,
        is_admin=is_admin,
    )
    return [OcorrenciaResponse(**item) for item in items]


@router.get('/{id}', response_model=OcorrenciaResponse)
async def get_occurrence(
    id: uuid.UUID,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
) -> OcorrenciaResponse:
    current_user_id = None
    is_admin = False

    if current_user:
        if current_user.get('user_id'):
            current_user_id = uuid.UUID(current_user['user_id'])
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        is_admin = any(p in papeis for p in ('sindico', 'administradora', 'subsindico', 'admin'))

    service = OcorrenciaService(db)
    item = await service.get_ocorrencia(
        ocorrencia_id=id,
        current_user_id=current_user_id,
        is_admin=is_admin,
    )
    return OcorrenciaResponse(**item)


@router.post(
    '', response_model=OcorrenciaResponse, status_code=status.HTTP_201_CREATED
)
async def create_occurrence(
    dto: OcorrenciaCreate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    registrada_por: uuid.UUID | None = Query(None),
) -> OcorrenciaResponse:
    target_condo_id = condominio_id
    target_user_id = registrada_por or dto.registrada_por or dto.usuario_id
    origem = dto.origem

    if current_user:
        if not target_condo_id and current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if not target_user_id and current_user.get('user_id'):
            target_user_id = uuid.UUID(current_user['user_id'])
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        if 'porteiro' in papeis and not dto.origem:
            origem = 'PORTARIA'
        elif 'morador' in papeis and not dto.origem:
            origem = 'MORADOR'

    service = OcorrenciaService(db)
    return await service.create_ocorrencia(
        dto,
        condominio_id=target_condo_id,
        registrada_por=target_user_id,
        origem=origem,
    )


@router.patch('/{id}/status', response_model=OcorrenciaResponse)
async def update_status(
    id: uuid.UUID,
    dto: OcorrenciaStatusUpdate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
) -> OcorrenciaResponse:
    autor_id = None
    if current_user and current_user.get('user_id'):
        autor_id = uuid.UUID(current_user['user_id'])

    service = OcorrenciaService(db)
    return await service.update_status(
        ocorrencia_id=id,
        novo_status=dto.status,
        mensagem=dto.mensagem,
        autor_id=autor_id,
    )


@router.post(
    '/{id}/eventos',
    response_model=HistoricoOcorrenciaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_evento(
    id: uuid.UUID,
    dto: HistoricoOcorrenciaCreate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
) -> HistoricoOcorrenciaResponse:
    autor_id = None
    if current_user and current_user.get('user_id'):
        autor_id = uuid.UUID(current_user['user_id'])

    service = OcorrenciaService(db)
    return await service.add_evento(
        ocorrencia_id=id,
        dto=dto,
        autor_id=autor_id,
    )

