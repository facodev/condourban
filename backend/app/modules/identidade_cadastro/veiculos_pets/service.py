import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Pet, Veiculo
from .schemas import PetCreate, VeiculoCreate
from app.modules.condominio.estrutura.models import Condominio, Unidade


class VeiculosPetsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _resolve_condominio_id(
        self, condominio_id: uuid.UUID | None, unidade_id: uuid.UUID
    ) -> uuid.UUID:
        if condominio_id:
            return condominio_id
        unidade = (
            await self.db.execute(select(Unidade).where(Unidade.id == unidade_id))
        ).scalar_one_or_none()
        if unidade and unidade.condominio_id:
            return unidade.condominio_id
        condo = (await self.db.execute(select(Condominio))).scalars().first()
        if condo:
            return condo.id
        return uuid.uuid4()

    async def cadastrar_veiculo(self, dto: VeiculoCreate) -> Veiculo:
        placa_limpa = dto.placa.strip().upper().replace('-', '').replace(' ', '')
        if not placa_limpa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='PLACA_INVALIDA',
            )

        c_id = await self._resolve_condominio_id(dto.condominio_id, dto.unidade_id)

        # Checar duplicidade no mesmo condomínio
        query_dup = select(Veiculo).where(
            Veiculo.condominio_id == c_id,
            Veiculo.placa == placa_limpa,
            Veiculo.status == 'ATIVO',
        )
        existente = (await self.db.execute(query_dup)).scalar_one_or_none()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='PLACA_DUPLICADA_NO_CONDOMINIO',
            )

        veiculo = Veiculo(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            proprietario_id=dto.proprietario_id,
            vaga_garagem_id=dto.vaga_garagem_id,
            placa=placa_limpa,
            tipo=dto.tipo,
            marca=dto.marca,
            modelo=dto.modelo,
            cor=dto.cor,
            status='ATIVO',
            observacao=dto.observacao,
        )
        self.db.add(veiculo)
        await self.db.commit()
        await self.db.refresh(veiculo)
        return veiculo

    async def listar_veiculos(
        self,
        condominio_id: uuid.UUID | None = None,
        unidade_id: uuid.UUID | None = None,
        unidade_ids: list[uuid.UUID] | None = None,
        placa: str | None = None,
    ) -> list[Veiculo]:
        stmt = select(Veiculo)
        if condominio_id:
            stmt = stmt.where(Veiculo.condominio_id == condominio_id)
        if unidade_id:
            stmt = stmt.where(Veiculo.unidade_id == unidade_id)
        elif unidade_ids is not None:
            if not unidade_ids:
                return []
            stmt = stmt.where(Veiculo.unidade_id.in_(unidade_ids))
        if placa:
            placa_limpa = placa.strip().upper().replace('-', '').replace(' ', '')
            stmt = stmt.where(Veiculo.placa == placa_limpa)
        stmt = stmt.order_by(Veiculo.criado_em.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def cadastrar_pet(self, dto: PetCreate) -> Pet:
        c_id = await self._resolve_condominio_id(dto.condominio_id, dto.unidade_id)
        pet = Pet(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            tutor_id=dto.tutor_id,
            nome=dto.nome.strip(),
            especie=dto.especie.upper(),
            raca=dto.raca,
            porte=dto.porte.upper(),
            cor=dto.cor,
            foto_url=dto.foto_url,
            vacinado=dto.vacinado,
            status='ATIVO',
            observacao=dto.observacao,
        )
        self.db.add(pet)
        await self.db.commit()
        await self.db.refresh(pet)
        return pet

    async def listar_pets(
        self,
        condominio_id: uuid.UUID | None = None,
        unidade_id: uuid.UUID | None = None,
        unidade_ids: list[uuid.UUID] | None = None,
    ) -> list[Pet]:
        stmt = select(Pet)
        if condominio_id:
            stmt = stmt.where(Pet.condominio_id == condominio_id)
        if unidade_id:
            stmt = stmt.where(Pet.unidade_id == unidade_id)
        elif unidade_ids is not None:
            if not unidade_ids:
                return []
            stmt = stmt.where(Pet.unidade_id.in_(unidade_ids))
        stmt = stmt.order_by(Pet.criado_em.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def remover_veiculo(self, veiculo_id: uuid.UUID) -> dict:
        veiculo = (
            await self.db.execute(select(Veiculo).where(Veiculo.id == veiculo_id))
        ).scalar_one_or_none()
        if not veiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='VEICULO_NAO_ENCONTRADO',
            )
        await self.db.delete(veiculo)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': 'Veículo excluído com sucesso.'}

    async def remover_pet(self, pet_id: uuid.UUID) -> dict:
        pet = (
            await self.db.execute(select(Pet).where(Pet.id == pet_id))
        ).scalar_one_or_none()
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='PET_NAO_ENCONTRADO',
            )
        await self.db.delete(pet)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': 'Animal doméstico excluído com sucesso.'}
