from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.comunicacao.mensageria.router import router as comunicados_router
from app.modules.comunicacao.ocorrencias.router import router as ocorrencias_router
from app.modules.comunicacao.router import router as comunicacao_router
from app.modules.identidade_cadastro.auth.router import login as auth_login_endpoint, router as auth_router
from app.modules.identidade_cadastro.auth.schemas import TokenResponse
from app.modules.condominio.router import router as condominio_router
from app.modules.controle_acesso.router import router as controle_acesso_router
from app.modules.governanca.router import router as governanca_router
from app.modules.identidade_cadastro.router import router as identidade_router


from app.modules.portaria.atendimento.router import router as visitantes_router
from app.modules.portaria.encomendas.router import router as encomendas_router
from app.modules.portaria.router import router as portaria_router
from app.modules.reservas.agendamentos.router import router as reservas_agendamentos_router
from app.modules.reservas.router import router as reservas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado na inicialização: registrar tabelas
    try:
        from app.core.database import engine, Base
        import app.modules.identidade_cadastro.pessoas.models  # noqa: F401
        import app.modules.identidade_cadastro.usuarios.models  # noqa: F401
        import app.modules.identidade_cadastro.auth.models  # noqa: F401
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
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            try:
                await conn.execute(text("ALTER TABLE pessoa ADD COLUMN telefones JSON DEFAULT '[]'"))
            except Exception:
                pass

        # Garantir integridade referencial: Inquilino SaaS e Condominios
        import uuid
        from sqlalchemy import select
        from app.core.database import async_session_maker
        from app.modules.condominio.branding.models import Inquilino, Condominio

        async with async_session_maker() as session:
            inquilino_res = await session.execute(select(Inquilino).limit(1))
            inq = inquilino_res.scalars().first()
            if not inq:
                inq = Inquilino(
                    id=uuid.uuid4(),
                    nome='CondoUrban Gestão e Tecnologia SaaS',
                    nome_fantasia='CondoUrban',
                    documento='12.345.678/0001-90',
                    status='ATIVO',
                )
                session.add(inq)
                await session.flush()

            all_inq_ids = set((await session.execute(select(Inquilino.id))).scalars().all())
            condos_res = await session.execute(select(Condominio))
            condos = condos_res.scalars().all()
            repaired = False
            for c in condos:
                if not c.inquilino_id or c.inquilino_id not in all_inq_ids:
                    c.inquilino_id = inq.id
                    repaired = True
            if repaired:
                await session.commit()
    except Exception as e:
        import logging
        logging.getLogger('uvicorn').warning(f'Aviso na inicialização do banco: {e}')
    yield
    # Executado no encerramento



app = FastAPI(
    title=settings.app_name,
    description=(
        'API do CondoUrban - Sistema de Gestão Inteligente para Condomínios'
    ),
    version='1.0.0',
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc',
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Health Check
@app.get('/health', tags=['Health'])
async def health_check() -> dict[str, str]:
    return {
        'status': 'healthy',
        'app': settings.app_name,
        'environment': settings.app_env,
    }


# Include Domain Routers via versioned API router
api_v1_router = APIRouter(prefix=settings.api_prefix)
api_v1_router.include_router(auth_router)
api_v1_router.add_api_route(
    '/identidade/users/login',
    auth_login_endpoint,
    methods=['POST'],
    response_model=TokenResponse,
    include_in_schema=False,
)
api_v1_router.include_router(condominio_router)
api_v1_router.include_router(identidade_router)
api_v1_router.include_router(controle_acesso_router)
api_v1_router.include_router(portaria_router)
api_v1_router.include_router(reservas_router)
api_v1_router.include_router(comunicacao_router)
api_v1_router.include_router(governanca_router)


# Routers de retrocompatibilidade para suportar contratos legados
acesso_router = APIRouter(prefix='/acesso', tags=['Acesso (Legado)'])
acesso_router.include_router(visitantes_router)
acesso_router.include_router(encomendas_router)
api_v1_router.include_router(acesso_router)

operacional_router = APIRouter(prefix='/operacional', tags=['Operacional (Legado)'])
operacional_router.include_router(reservas_agendamentos_router)
operacional_router.include_router(ocorrencias_router)
operacional_router.include_router(comunicados_router)
api_v1_router.include_router(operacional_router)

app.include_router(api_v1_router)
