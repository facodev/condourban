"""Camada de compatibilidade retroativa para app.modules.condominio.estrutura.schemas.

Os schemas foram segregados nos submódulos canônicos:
- app.modules.condominio.branding.schemas
- app.modules.condominio.blocos_unidades.schemas
- app.modules.condominio.vagas.schemas
"""

from app.modules.condominio.blocos_unidades.schemas import (
    BlockResponse,
    BlocoBase,
    BlocoCreate,
    BlocoResponse,
    BlocoUpdate,
    UnidadeBase,
    UnidadeCreate,
    UnidadeResponse,
    UnidadeUpdate,
    UnitResponse,
)
from app.modules.condominio.branding.schemas import (
    CondominioInfoResponse,
    CondominioInfoUpdate,
    ConfiguracaoCondominioUpdate,
)
from app.modules.condominio.vagas.schemas import (
    VagaGaragemBase,
    VagaGaragemCreate,
    VagaGaragemResponse,
    VagaGaragemUpdate,
)

__all__ = [
    'BlocoBase',
    'BlocoCreate',
    'BlocoUpdate',
    'BlocoResponse',
    'UnidadeBase',
    'UnidadeCreate',
    'UnidadeUpdate',
    'UnidadeResponse',
    'VagaGaragemBase',
    'VagaGaragemCreate',
    'VagaGaragemUpdate',
    'VagaGaragemResponse',
    'CondominioInfoResponse',
    'CondominioInfoUpdate',
    'ConfiguracaoCondominioUpdate',
    'BlockResponse',
    'UnitResponse',
]
