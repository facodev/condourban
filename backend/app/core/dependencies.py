import uuid
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login'
)
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    auto_error=False,
)

# Reusable Session Dependency as recommended by FastAPI skill
SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_active_condominio_id(
    db: SessionDep,
    condominio_id: uuid.UUID | None = Query(None, alias='condominio_id'),
    x_condominio_id: str | None = Header(None, alias='X-Condominio-Id'),
    x_tenant_id: str | None = Header(None, alias='X-Tenant-Id'),
) -> uuid.UUID | None:
    """Extrai o condomínio ativo da requisição (Query param > Header X-Condominio-Id > X-Tenant-Id > db.info)."""
    resolved_id: uuid.UUID | None = None

    if condominio_id:
        resolved_id = condominio_id
    elif x_condominio_id or x_tenant_id:
        val = x_condominio_id or x_tenant_id
        try:
            resolved_id = uuid.UUID(val)
        except (ValueError, TypeError):
            resolved_id = None
    elif 'condominio_id' in db.info:
        try:
            resolved_id = uuid.UUID(str(db.info['condominio_id']))
        except (ValueError, TypeError):
            resolved_id = None

    if resolved_id:
        if db.bind and db.bind.dialect.name == 'postgresql':
            from sqlalchemy import text
            try:
                await db.execute(text(f"SET LOCAL app.condominio_id = '{resolved_id}'"))
            except Exception:
                pass
        db.info['condominio_id'] = str(resolved_id)

    return resolved_id


ActiveCondominioDep = Annotated[uuid.UUID | None, Depends(get_active_condominio_id)]


async def get_database() -> AsyncSession:
    """Função utilitária legada / retrocompatibilidade."""
    async for session in get_db():
        return session


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: SessionDep,
    x_condominio_id: Annotated[str | None, Header(alias='X-Condominio-Id')] = None,
    x_tenant_id: Annotated[str | None, Header(alias='X-Tenant-Id')] = None,
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='CREDENCIAIS_INVALIDAS',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str | None = payload.get('sub')
    if user_id is None:
        raise credentials_exception

    # Preferência: Header ativo explicitado pelo usuário/sessão, senão claim do token
    condominio_id: str | None = x_condominio_id or x_tenant_id or payload.get('condominio_id')
    papeis: list[str] = payload.get('papeis', [])

    if condominio_id:
        try:
            if db.bind and db.bind.dialect.name == 'postgresql':
                from sqlalchemy import text
                await db.execute(text(f"SET LOCAL app.condominio_id = '{condominio_id}'"))
            db.info['condominio_id'] = str(condominio_id)
        except Exception:
            pass

    return {
        'user_id': user_id,
        'condominio_id': condominio_id,
        'papeis': papeis,
        'email': payload.get('email'),
        'pessoa_id': payload.get('pessoa_id'),
        'unidade_ids': payload.get('unidade_ids') or [],
    }


async def get_current_user_optional(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)],
    db: SessionDep,
) -> dict | None:
    if not token:
        return None
    return await get_current_user(token, db)


# Reusable CurrentUser Dependency
CurrentUserDep = Annotated[dict, Depends(get_current_user)]
OptionalCurrentUserDep = Annotated[dict | None, Depends(get_current_user_optional)]
