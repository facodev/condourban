from fastapi import APIRouter

from .agendamentos.router import router as agendamentos_router

router = APIRouter(tags=['Reservas'])
router.include_router(agendamentos_router)
