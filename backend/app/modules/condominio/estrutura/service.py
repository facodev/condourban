"""Camada de compatibilidade retroativa para EstruturaService.

Delega internamente para:
- BrandingService
- BlocosUnidadesService
- VagasService
"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.condominio.blocos_unidades.models import Bloco, Unidade
from app.modules.condominio.blocos_unidades.schemas import (
    BlocoCreate,
    BlocoUpdate,
    UnidadeCreate,
    UnidadeUpdate,
)
from app.modules.condominio.blocos_unidades.service import BlocosUnidadesService
from app.modules.condominio.branding.models import Condominio
from app.modules.condominio.branding.schemas import (
    CondominioInfoUpdate,
    ConfiguracaoCondominioUpdate,
)
from app.modules.condominio.branding.service import BrandingService
from app.modules.condominio.vagas.models import VagaGaragem
from app.modules.condominio.vagas.schemas import (
    VagaGaragemCreate,
    VagaGaragemUpdate,
)
from app.modules.condominio.vagas.service import VagasService


class EstruturaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.branding_service = BrandingService(db)
        self.blocos_unidades_service = BlocosUnidadesService(db)
        self.vagas_service = VagasService(db)

    # Blocos
    async def list_blocos(self, condominio_id: uuid.UUID | None = None) -> list[Bloco]:
        return await self.blocos_unidades_service.list_blocos(condominio_id)

    async def create_bloco(
        self, dto: BlocoCreate, condominio_id: uuid.UUID | None = None
    ) -> Bloco:
        return await self.blocos_unidades_service.create_bloco(dto, condominio_id)

    async def update_bloco(
        self, bloco_id: uuid.UUID, dto: BlocoUpdate
    ) -> Bloco:
        return await self.blocos_unidades_service.update_bloco(bloco_id, dto)

    async def delete_bloco(self, bloco_id: uuid.UUID) -> dict:
        return await self.blocos_unidades_service.delete_bloco(bloco_id)

    # Unidades
    async def list_unidades(
        self,
        condominio_id: uuid.UUID | None = None,
        bloco_id: uuid.UUID | None = None,
    ) -> list[Unidade]:
        return await self.blocos_unidades_service.list_unidades(condominio_id, bloco_id)

    async def create_unidade(
        self, dto: UnidadeCreate, condominio_id: uuid.UUID | None = None
    ) -> Unidade:
        return await self.blocos_unidades_service.create_unidade(dto, condominio_id)

    async def update_unidade(
        self, unidade_id: uuid.UUID, dto: UnidadeUpdate
    ) -> Unidade:
        return await self.blocos_unidades_service.update_unidade(unidade_id, dto)

    async def delete_unidade(self, unidade_id: uuid.UUID) -> dict:
        return await self.blocos_unidades_service.delete_unidade(unidade_id)

    async def importar_unidades_csv(
        self, conteudo_csv: str, condominio_id: uuid.UUID | None = None
    ) -> dict:
        return await self.blocos_unidades_service.importar_unidades_csv(conteudo_csv, condominio_id)

    # Vagas
    async def list_vagas(
        self,
        condominio_id: uuid.UUID | None = None,
        unidade_id: uuid.UUID | None = None,
    ) -> list[VagaGaragem]:
        return await self.vagas_service.list_vagas(condominio_id, unidade_id)

    async def create_vaga(
        self, dto: VagaGaragemCreate, condominio_id: uuid.UUID | None = None
    ) -> VagaGaragem:
        return await self.vagas_service.create_vaga(dto, condominio_id)

    async def update_vaga(
        self, vaga_id: uuid.UUID, dto: VagaGaragemUpdate
    ) -> VagaGaragem:
        return await self.vagas_service.update_vaga(vaga_id, dto)

    async def delete_vaga(self, vaga_id: uuid.UUID) -> dict:
        return await self.vagas_service.delete_vaga(vaga_id)

    # Branding & Institucional
    async def get_or_create_condominio(
        self, condominio_id: uuid.UUID | None = None
    ) -> Condominio:
        return await self.branding_service.get_or_create_condominio(condominio_id)

    async def update_condominio_info(
        self, condominio_id: uuid.UUID | None, dto: CondominioInfoUpdate
    ) -> Condominio:
        return await self.branding_service.update_condominio_info(condominio_id, dto)

    async def get_configuracoes(
        self, condominio_id: uuid.UUID | None = None
    ) -> dict:
        return await self.branding_service.get_configuracoes(condominio_id)

    async def update_configuracoes(
        self, condominio_id: uuid.UUID | None, dto: ConfiguracaoCondominioUpdate
    ) -> dict:
        return await self.branding_service.update_configuracoes(condominio_id, dto)

    async def list_condominios(self) -> list[Condominio]:
        return await self.branding_service.list_condominios()

    async def create_condominio(self, dto: CondominioInfoUpdate) -> Condominio:
        return await self.branding_service.create_condominio(dto)

    async def delete_condominio(self, condominio_id: uuid.UUID) -> dict:
        return await self.branding_service.delete_condominio(condominio_id)
