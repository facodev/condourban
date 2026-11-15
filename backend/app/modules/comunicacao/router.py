from fastapi import APIRouter

from .fale_conosco.router import router as fale_conosco_router
from .mensageria.router import router as mensageria_router
from .ocorrencias.router import router as ocorrencias_router

router = APIRouter(prefix='/comunicacao', tags=['Comunicação'])
router.include_router(mensageria_router)
router.include_router(ocorrencias_router)
router.include_router(fale_conosco_router)

