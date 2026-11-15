import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool
from starlette.requests import Request

# Import all models to register with Base.metadata
import app.modules.identidade_cadastro.pessoas.models  # noqa: F401
import app.modules.identidade_cadastro.usuarios.models  # noqa: F401
import app.modules.identidade_cadastro.onboarding.models  # noqa: F401
import app.modules.identidade_cadastro.veiculos_pets.models  # noqa: F401
import app.modules.condominio.branding.models  # noqa: F401
import app.modules.condominio.blocos_unidades.models  # noqa: F401
import app.modules.condominio.vagas.models  # noqa: F401
import app.modules.condominio.estrutura.models  # noqa: F401
import app.modules.condominio.areas_comuns.models  # noqa: F401
import app.modules.controle_acesso.dispositivos.models  # noqa: F401
import app.modules.controle_acesso.credenciais.models  # noqa: F401
import app.modules.controle_acesso.eventos_acesso.models  # noqa: F401
import app.modules.portaria.atendimento.models  # noqa: F401
import app.modules.portaria.encomendas.models  # noqa: F401
import app.modules.reservas.agendamentos.models  # noqa: F401
import app.modules.reservas.vistorias.models  # noqa: F401
import app.modules.comunicacao.mensageria.models  # noqa: F401
import app.modules.comunicacao.ocorrencias.models  # noqa: F401
import app.modules.comunicacao.mural_social.models  # noqa: F401
import app.modules.governanca.assembleias.models  # noqa: F401
import app.modules.governanca.seguranca_auditoria.models  # noqa: F401
import app.modules.financeiro.cobrancas_acordos.models  # noqa: F401
import app.modules.financeiro.despesas_medicoes.models  # noqa: F401
import app.modules.manutencao.chamados_servicos.models  # noqa: F401
import app.modules.manutencao.plano_inventario.models  # noqa: F401

from app.core.database import Base, get_db
from app.core.dependencies import get_current_user
from app.core.security import decode_access_token
from app.main import app

TEST_DATABASE_URL = 'sqlite+aiosqlite://'

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

DEFAULT_TEST_USER = {
    'user_id': str(uuid.uuid4()),
    'condominio_id': None,
    'papeis': ['ADMINISTRADOR', 'SINDICO'],
    'email': 'pytest.admin@condourban.com',
    'pessoa_id': None,
    'unidade_ids': [],
}


@pytest.fixture(autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client():
    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def override_get_current_user(request: Request) -> dict:
        """Aceita Bearer real; sem token, assume gestão (compatível com testes BC-01/02)."""
        auth = request.headers.get('Authorization') or request.headers.get('authorization')
        if auth and auth.lower().startswith('bearer '):
            token = auth.split(' ', 1)[1].strip()
            payload = decode_access_token(token)
            if payload is None:
                from fastapi import HTTPException, status

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='CREDENCIAIS_INVALIDAS',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            condo = (
                request.headers.get('X-Condominio-Id')
                or request.headers.get('X-Tenant-Id')
                or payload.get('condominio_id')
            )
            return {
                'user_id': payload.get('sub'),
                'condominio_id': condo,
                'papeis': payload.get('papeis', []),
                'email': payload.get('email'),
                'pessoa_id': payload.get('pessoa_id'),
                'unidade_ids': payload.get('unidade_ids') or [],
            }
        return dict(DEFAULT_TEST_USER)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url='http://test'
    ) as client:
        yield client
    app.dependency_overrides.clear()
