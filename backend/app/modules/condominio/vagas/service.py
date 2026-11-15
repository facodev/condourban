import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import VagaGaragem
from .schemas import VagaGaragemCreate, VagaGaragemUpdate


class VagasService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_vagas(
        self,
        condominio_id: uuid.UUID | None = None,
        unidade_id: uuid.UUID | None = None,
    ) -> list[VagaGaragem]:
        stmt = select(VagaGaragem)
        if condominio_id:
            stmt = stmt.where(VagaGaragem.condominio_id == condominio_id)
        if unidade_id:
            stmt = stmt.where(VagaGaragem.unidade_id == unidade_id)
        stmt = stmt.order_by(VagaGaragem.identificacao.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_vaga(
        self, dto: VagaGaragemCreate, condominio_id: uuid.UUID | None = None
    ) -> VagaGaragem:
        c_id = dto.condominio_id or condominio_id
        if not c_id and dto.unidade_id:
            from app.modules.condominio.blocos_unidades.models import Unidade

            u = (
                await self.db.execute(
                    select(Unidade).where(Unidade.id == dto.unidade_id)
                )
            ).scalar_one_or_none()
            if u and u.condominio_id:
                c_id = u.condominio_id
        if not c_id:
            from app.modules.condominio.branding.models import Condominio

            first_c = (await self.db.execute(select(Condominio))).scalars().first()
            c_id = first_c.id if first_c else uuid.uuid4()

        dup = (
            await self.db.execute(
                select(VagaGaragem).where(
                    VagaGaragem.condominio_id == c_id,
                    VagaGaragem.identificacao == dto.identificacao,
                    VagaGaragem.status == 'ATIVO',
                )
            )
        ).scalar_one_or_none()
        if dup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='VAGA_DUPLICADA',
            )

        vaga = VagaGaragem(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            identificacao=dto.identificacao,
            tipo=dto.tipo,
            coberta=dto.coberta,
            status='ATIVO',
        )
        self.db.add(vaga)
        await self.db.commit()
        await self.db.refresh(vaga)
        return vaga

    async def update_vaga(
        self, vaga_id: uuid.UUID, dto: VagaGaragemUpdate
    ) -> VagaGaragem:
        vaga = (
            await self.db.execute(
                select(VagaGaragem).where(VagaGaragem.id == vaga_id)
            )
        ).scalar_one_or_none()
        if not vaga:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='VAGA_NAO_ENCONTRADA',
            )

        if dto.identificacao is not None:
            identificacao_limpa = dto.identificacao.strip()
            if not identificacao_limpa:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='IDENTIFICACAO_OBRIGATORIA',
                )
            if identificacao_limpa != vaga.identificacao:
                dup = (
                    await self.db.execute(
                        select(VagaGaragem).where(
                            (VagaGaragem.condominio_id == vaga.condominio_id if vaga.condominio_id is not None else VagaGaragem.condominio_id.is_(None)),
                            VagaGaragem.identificacao == identificacao_limpa,
                            VagaGaragem.status == 'ATIVO',
                            VagaGaragem.id != vaga.id,
                        )
                    )
                ).scalar_one_or_none()
                if dup:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='VAGA_DUPLICADA',
                    )
                vaga.identificacao = identificacao_limpa

        if dto.unidade_id is not None:
            vaga.unidade_id = dto.unidade_id
        if dto.tipo is not None:
            vaga.tipo = dto.tipo
        if dto.coberta is not None:
            vaga.coberta = dto.coberta

        await self.db.commit()
        await self.db.refresh(vaga)
        return vaga

    async def delete_vaga(self, vaga_id: uuid.UUID) -> dict:
        vaga = (
            await self.db.execute(select(VagaGaragem).where(VagaGaragem.id == vaga_id))
        ).scalar_one_or_none()
        if not vaga:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='VAGA_NAO_ENCONTRADA',
            )

        await self.db.delete(vaga)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': f'Vaga {vaga.identificacao} excluída com sucesso.'}

