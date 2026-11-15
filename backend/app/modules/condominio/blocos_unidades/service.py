import csv
import io
import uuid
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Bloco, Unidade
from .schemas import BlocoCreate, BlocoUpdate, UnidadeCreate, UnidadeUpdate


class BlocosUnidadesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_blocos(self, condominio_id: uuid.UUID | None = None) -> list[Bloco]:
        query = select(Bloco)
        if condominio_id:
            query = query.where(Bloco.condominio_id == condominio_id)
        query = query.order_by(Bloco.ordem.asc(), Bloco.nome.asc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_blocos_por_unidades(
        self,
        unidade_ids: list[uuid.UUID],
        condominio_id: uuid.UUID | None = None,
    ) -> list[Bloco]:
        if not unidade_ids:
            return []
        bloco_ids = (
            await self.db.execute(
                select(Unidade.bloco_id).where(
                    Unidade.id.in_(unidade_ids),
                    Unidade.bloco_id.is_not(None),
                )
            )
        ).scalars().all()
        ids = list({b for b in bloco_ids if b})
        if not ids:
            return []
        query = select(Bloco).where(Bloco.id.in_(ids))
        if condominio_id:
            query = query.where(Bloco.condominio_id == condominio_id)
        query = query.order_by(Bloco.ordem.asc(), Bloco.nome.asc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_bloco(
        self, dto: BlocoCreate, condominio_id: uuid.UUID | None = None
    ) -> Bloco:
        c_id = dto.condominio_id or condominio_id or uuid.uuid4()
        dup = (
            await self.db.execute(
                select(Bloco).where(
                    Bloco.condominio_id == c_id,
                    Bloco.nome == dto.nome,
                    Bloco.status == 'ATIVO',
                )
            )
        ).scalar_one_or_none()
        if dup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='BLOCO_DUPLICADO',
            )

        bloco = Bloco(
            condominio_id=c_id,
            nome=dto.nome,
            descricao=dto.descricao,
            ordem=dto.ordem,
            status='ATIVO',
        )
        self.db.add(bloco)
        await self.db.commit()
        await self.db.refresh(bloco)
        return bloco

    async def update_bloco(
        self, bloco_id: uuid.UUID, dto: BlocoUpdate
    ) -> Bloco:
        bloco = (
            await self.db.execute(select(Bloco).where(Bloco.id == bloco_id))
        ).scalar_one_or_none()
        if not bloco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='BLOCO_NAO_ENCONTRADO',
            )
        if dto.nome is not None and dto.nome != bloco.nome:
            dup = (
                await self.db.execute(
                    select(Bloco).where(
                        Bloco.condominio_id == bloco.condominio_id,
                        Bloco.nome == dto.nome,
                        Bloco.status == 'ATIVO',
                        Bloco.id != bloco.id,
                    )
                )
            ).scalar_one_or_none()
            if dup:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='BLOCO_DUPLICADO',
                )
            bloco.nome = dto.nome
        if dto.descricao is not None:
            bloco.descricao = dto.descricao
        if dto.ordem is not None:
            bloco.ordem = dto.ordem
        if dto.status is not None:
            bloco.status = dto.status

        await self.db.commit()
        await self.db.refresh(bloco)
        return bloco

    async def delete_bloco(self, bloco_id: uuid.UUID) -> dict:
        bloco = (
            await self.db.execute(select(Bloco).where(Bloco.id == bloco_id))
        ).scalar_one_or_none()
        if not bloco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='BLOCO_NAO_ENCONTRADO',
            )

        qtd_unidades = (
            await self.db.execute(
                select(func.count(Unidade.id)).where(Unidade.bloco_id == bloco_id)
            )
        ).scalar_one()
        if qtd_unidades > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'BLOCO_POSSUI_UNIDADES: Não é possível excluir o bloco "{bloco.nome}" pois ele possui {qtd_unidades} unidade(s) vinculada(s). Exclua ou mova as unidades primeiro.',
            )

        await self.db.delete(bloco)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': f'Bloco {bloco.nome} excluído com sucesso.'}

    async def list_unidades(
        self,
        condominio_id: uuid.UUID | None = None,
        bloco_id: uuid.UUID | None = None,
        unidade_ids: list[uuid.UUID] | None = None,
    ) -> list[Unidade]:
        query = select(Unidade)
        if condominio_id:
            query = query.where(Unidade.condominio_id == condominio_id)
        if bloco_id:
            query = query.where(Unidade.bloco_id == bloco_id)
        if unidade_ids is not None:
            if not unidade_ids:
                return []
            query = query.where(Unidade.id.in_(unidade_ids))
        query = query.order_by(Unidade.identificacao.asc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_unidade(
        self, dto: UnidadeCreate, condominio_id: uuid.UUID | None = None
    ) -> Unidade:
        c_id = dto.condominio_id or condominio_id

        if dto.bloco_id:
            b_query = select(Bloco).where(Bloco.id == dto.bloco_id)
            bloco_obj = (await self.db.execute(b_query)).scalar_one_or_none()
            if bloco_obj:
                c_id = bloco_obj.condominio_id

        c_id = c_id or uuid.uuid4()

        dup_query = select(Unidade).where(
            Unidade.identificacao == dto.identificacao,
            Unidade.status == 'ATIVO',
        )
        if dto.bloco_id:
            dup_query = dup_query.where(Unidade.bloco_id == dto.bloco_id)
        else:
            dup_query = dup_query.where(Unidade.condominio_id == c_id)

        existing = (await self.db.execute(dup_query)).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='UNIDADE_DUPLICADA',
            )

        unidade = Unidade(
            condominio_id=c_id,
            bloco_id=dto.bloco_id,
            identificacao=dto.identificacao,
            andar=dto.andar,
            tipo=dto.tipo,
            descricao=dto.descricao,
            area_privativa=dto.area_privativa,
            status='ATIVO',
        )
        self.db.add(unidade)
        await self.db.commit()
        await self.db.refresh(unidade)
        return unidade

    async def update_unidade(
        self, unidade_id: uuid.UUID, dto: UnidadeUpdate
    ) -> Unidade:
        unidade = (
            await self.db.execute(select(Unidade).where(Unidade.id == unidade_id))
        ).scalar_one_or_none()
        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='UNIDADE_NAO_ENCONTRADA',
            )
        if dto.identificacao is not None:
            unidade.identificacao = dto.identificacao
        if dto.andar is not None:
            unidade.andar = dto.andar
        if dto.bloco_id is not None:
            unidade.bloco_id = dto.bloco_id
        if dto.tipo is not None:
            unidade.tipo = dto.tipo
        if dto.descricao is not None:
            unidade.descricao = dto.descricao
        if dto.area_privativa is not None:
            unidade.area_privativa = dto.area_privativa
        if dto.status is not None:
            unidade.status = dto.status

        await self.db.commit()
        await self.db.refresh(unidade)
        return unidade

    async def delete_unidade(self, unidade_id: uuid.UUID) -> dict:
        from app.modules.identidade_cadastro.usuarios.models import OcupacaoUnidade
        from app.modules.identidade_cadastro.veiculos_pets.models import Veiculo, Pet

        unidade = (
            await self.db.execute(select(Unidade).where(Unidade.id == unidade_id))
        ).scalar_one_or_none()
        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='UNIDADE_NAO_ENCONTRADA',
            )

        # 1. Checar ocupações ativas
        ocup = (
            await self.db.execute(
                select(OcupacaoUnidade).where(
                    OcupacaoUnidade.unidade_id == unidade_id,
                    OcupacaoUnidade.status == 'ATIVA',
                )
            )
        ).scalar_one_or_none()
        if ocup:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'UNIDADE_POSSUI_OCUPACOES: A unidade {unidade.identificacao} possui moradores ou ocupações ativas. Inative ou remova os vínculos antes de excluir.',
            )

        # 2. Checar veículos cadastrados
        veic = (
            await self.db.execute(
                select(Veiculo).where(Veiculo.unidade_id == unidade_id)
            )
        ).scalar_one_or_none()
        if veic:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'UNIDADE_POSSUI_VEICULOS: A unidade {unidade.identificacao} possui veículos vinculados. Remova os veículos primeiro.',
            )

        # 3. Checar pets
        pet = (
            await self.db.execute(
                select(Pet).where(Pet.unidade_id == unidade_id)
            )
        ).scalar_one_or_none()
        if pet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'UNIDADE_POSSUI_PETS: A unidade {unidade.identificacao} possui animais de estimação vinculados. Remova os pets primeiro.',
            )

        # Desvincular vagas de garagem associadas
        try:
            from app.modules.condominio.vagas.models import VagaGaragem

            vagas = (
                await self.db.execute(
                    select(VagaGaragem).where(VagaGaragem.unidade_id == unidade_id)
                )
            ).scalars().all()
            for v in vagas:
                v.unidade_id = None
        except Exception:
            pass

        # Excluir ocupações inativas históricas
        hist = (
            await self.db.execute(
                select(OcupacaoUnidade).where(OcupacaoUnidade.unidade_id == unidade_id)
            )
        ).scalars().all()
        for h in hist:
            await self.db.delete(h)

        await self.db.delete(unidade)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': f'Unidade {unidade.identificacao} excluída com sucesso.'}

    async def importar_unidades_csv(
        self, conteudo_csv: str, condominio_id: uuid.UUID | None = None
    ) -> dict:
        c_id = condominio_id or uuid.uuid4()
        reader = csv.DictReader(io.StringIO(conteudo_csv))
        criadas = 0
        erros = []
        for idx, row in enumerate(reader):
            identificacao = row.get('identificacao') or row.get('numero')
            if not identificacao:
                erros.append(f'Linha {idx+1}: identificacao ausente')
                continue
            bloco_nome = row.get('bloco')
            bloco_id = None
            if bloco_nome:
                b_query = select(Bloco).where(
                    Bloco.condominio_id == c_id, Bloco.nome == bloco_nome
                )
                bloco = (await self.db.execute(b_query)).scalar_one_or_none()
                if not bloco:
                    bloco = Bloco(
                        condominio_id=c_id, nome=bloco_nome, status='ATIVO'
                    )
                    self.db.add(bloco)
                    await self.db.flush()
                bloco_id = bloco.id
            u = Unidade(
                condominio_id=c_id,
                bloco_id=bloco_id,
                identificacao=identificacao,
                andar=int(row['andar'])
                if row.get('andar') and str(row['andar']).isdigit()
                else None,
                status='ATIVO',
            )
            self.db.add(u)
            criadas += 1
        await self.db.commit()
        return {'unidades_criadas': criadas, 'erros': erros}

