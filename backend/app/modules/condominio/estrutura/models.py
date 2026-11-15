"""Camada de compatibilidade retroativa para app.modules.condominio.estrutura.models.

Os modelos foram segregados nos submódulos canônicos:
- app.modules.condominio.branding.models (Condominio, Inquilino)
- app.modules.condominio.blocos_unidades.models (Bloco, Unidade, Block, Unit)
- app.modules.condominio.vagas.models (VagaGaragem)
"""

from app.modules.condominio.blocos_unidades.models import Block, Bloco, Unidade, Unit
from app.modules.condominio.branding.models import Condominio, Inquilino
from app.modules.condominio.vagas.models import VagaGaragem

__all__ = [
    'Inquilino',
    'Condominio',
    'Bloco',
    'Unidade',
    'VagaGaragem',
    'Block',
    'Unit',
]
