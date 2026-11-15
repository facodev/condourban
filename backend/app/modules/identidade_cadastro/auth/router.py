from typing import Annotated
import uuid
from fastapi import APIRouter, Header, Request, status

from app.core.dependencies import CurrentUserDep, SessionDep
from .schemas import (
    GoogleLoginRequest,
    LoginRequest,
    SelecionarCondominioRequest,
    TokenResponse,
)
from .service import AuthService

router = APIRouter(prefix='/auth', tags=['Autenticação'])


@router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    dto: LoginRequest,
    db: SessionDep,
    request: Request,
    x_correlation_id: Annotated[str | None, Header()] = None,
) -> TokenResponse:
    ip = request.client.host if request.client else None
    service = AuthService(db)
    return await service.authenticate(dto, ip=ip, id_correlacao=x_correlation_id)


@router.post('/google', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def google_login(
    dto: GoogleLoginRequest,
    db: SessionDep,
    request: Request,
    x_correlation_id: Annotated[str | None, Header()] = None,
) -> TokenResponse:
    ip = request.client.host if request.client else None
    service = AuthService(db)
    return await service.authenticate_google(dto, ip=ip, id_correlacao=x_correlation_id)


@router.post(
    '/selecionar-condominio',
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def selecionar_condominio(
    dto: SelecionarCondominioRequest,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> TokenResponse:
    service = AuthService(db)
    user_id = uuid.UUID(current_user['user_id'])
    return await service.selecionar_condominio(user_id, dto.condominio_id)
