from fastapi import APIRouter

from .areas_comuns.router import (
    router as areas_comuns_router,
)
from .blocos_unidades.router import (
    router as blocos_unidades_router,
)
from .branding.router import (
    router as branding_router,
)
from .vagas.router import (
    router as vagas_router,
)

router = APIRouter(prefix='/condominio')
router.include_router(branding_router)
router.include_router(blocos_unidades_router)
router.include_router(vagas_router)
router.include_router(areas_comuns_router)
