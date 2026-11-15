from fastapi import APIRouter

from .atendimento.router import router as atendimento_router
from .encomendas.router import router as encomendas_router

router = APIRouter(prefix='/portaria', tags=['Portaria'])
router.include_router(atendimento_router)
router.include_router(encomendas_router)
