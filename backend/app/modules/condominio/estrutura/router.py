"""Camada de compatibilidade retroativa para app.modules.condominio.estrutura.router."""

from fastapi import APIRouter

from app.modules.condominio.blocos_unidades.router import (
    router as blocos_unidades_router,
)
from app.modules.condominio.branding.router import (
    router as branding_router,
)
from app.modules.condominio.vagas.router import (
    router as vagas_router,
)

router = APIRouter()
router.include_router(branding_router)
router.include_router(blocos_unidades_router)
router.include_router(vagas_router)
