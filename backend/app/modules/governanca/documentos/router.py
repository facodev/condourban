import uuid
from fastapi import APIRouter, HTTPException, Query, status

from app.core.dependencies import OptionalCurrentUserDep, SessionDep
from .schemas import (
    AlertaVencimentoResponse,
    DocumentoCreate,
    DocumentoResponse,
    DownloadResponse,
    PastaDocumentoCreate,
    PastaDocumentoResponse,
)
from .service import DocumentosService

router = APIRouter(prefix='/documentos', tags=['Governança - Documentos'])


@router.post('/pastas', response_model=PastaDocumentoResponse, status_code=status.HTTP_201_CREATED)
async def create_pasta(
    dto: PastaDocumentoCreate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
) -> PastaDocumentoResponse:
    target_condo_id = condominio_id
    if current_user and current_user.get('condominio_id'):
        target_condo_id = uuid.UUID(current_user['condominio_id'])

    service = DocumentosService(db)
    return await service.create_pasta(dto, condominio_id=target_condo_id)


@router.get('/pastas', response_model=list[PastaDocumentoResponse])
async def list_pastas(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
) -> list[PastaDocumentoResponse]:
    target_condo_id = condominio_id
    if current_user and current_user.get('condominio_id'):
        target_condo_id = uuid.UUID(current_user['condominio_id'])

    service = DocumentosService(db)
    return await service.list_pastas(condominio_id=target_condo_id)


@router.get('/alertas-vencimento', response_model=list[AlertaVencimentoResponse])
async def list_alertas_vencimento(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
) -> list[AlertaVencimentoResponse]:
    target_condo_id = condominio_id
    if current_user and current_user.get('condominio_id'):
        target_condo_id = uuid.UUID(current_user['condominio_id'])

    service = DocumentosService(db)
    items = await service.list_alertas_vencimento(condominio_id=target_condo_id)
    return [AlertaVencimentoResponse(**item) for item in items]


@router.get('', response_model=list[DocumentoResponse])
async def list_documentos(
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
    pasta_id: uuid.UUID | None = Query(None),
) -> list[DocumentoResponse]:
    target_condo_id = condominio_id
    if current_user and current_user.get('condominio_id'):
        target_condo_id = uuid.UUID(current_user['condominio_id'])

    service = DocumentosService(db)
    return await service.list_documentos(condominio_id=target_condo_id, pasta_id=pasta_id)


@router.post('', response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED)
async def create_documento(
    dto: DocumentoCreate,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
    condominio_id: uuid.UUID | None = Query(None),
) -> DocumentoResponse:
    target_condo_id = condominio_id
    enviado_por = None
    if current_user:
        if current_user.get('condominio_id'):
            target_condo_id = uuid.UUID(current_user['condominio_id'])
        if current_user.get('user_id'):
            enviado_por = uuid.UUID(current_user['user_id'])
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        is_gestao = any(p in papeis for p in ('sindico', 'administradora', 'subsindico', 'admin'))
        if 'morador' in papeis and not is_gestao:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='PERMISSAO_NEGADA',
            )

    service = DocumentosService(db)
    return await service.create_documento(
        dto, condominio_id=target_condo_id, enviado_por=enviado_por
    )


@router.get('/{id}/download', response_model=DownloadResponse)
async def download_documento(
    id: uuid.UUID,
    db: SessionDep,
    current_user: OptionalCurrentUserDep = None,
) -> DownloadResponse:
    is_admin = False
    if current_user:
        papeis = [p.lower() for p in current_user.get('papeis', [])]
        is_admin = any(p in papeis for p in ('sindico', 'administradora', 'subsindico', 'admin'))

    service = DocumentosService(db)
    info = await service.get_download_info(documento_id=id, is_admin=is_admin)
    return DownloadResponse(**info)
