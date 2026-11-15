from fastapi import APIRouter

from .onboarding.router import router as onboarding_router
from .pessoas.router import router as pessoas_router
from .usuarios.router import ocupacoes_router, router as usuarios_router
from .veiculos_pets.router import router as veiculos_pets_router

router = APIRouter(prefix='/identidade', tags=['Identidade e Cadastro'])
router.include_router(usuarios_router)
router.include_router(ocupacoes_router)
router.include_router(pessoas_router)
router.include_router(onboarding_router)
router.include_router(veiculos_pets_router)

