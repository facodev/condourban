from fastapi import APIRouter

from .documentos.router import router as documentos_router

router = APIRouter(prefix='/governanca', tags=['Governança'])
router.include_router(documentos_router)
