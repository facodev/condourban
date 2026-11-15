from datetime import datetime, timedelta, timezone
from typing import Any
import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Comunicado, LeituraComunicado, MensagemFaleConosco
from .schemas import ComunicadoCreate, MensagemFaleConoscoCreate


class ComunicadoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_comunicados(
        self,
        condominio_id: uuid.UUID | None = None,
        pessoa_id: uuid.UUID | None = None,
    ) -> list[dict[str, Any]]:
        query = select(Comunicado).options(selectinload(Comunicado.leituras))
        if condominio_id:
            query = query.where(Comunicado.condominio_id == condominio_id)
        result = await self.db.execute(query)
        comunicados = list(result.scalars().all())

        items = []
        for c in comunicados:
            lido = False
            if pessoa_id:
                lido = any(str(l.pessoa_id) == str(pessoa_id) for l in c.leituras)
            item_dict = {
                'id': c.id,
                'condominio_id': c.condominio_id,
                'titulo': c.titulo,
                'conteudo': c.conteudo,
                'autor_id': c.autor_id,
                'urgente': c.urgente,
                'fixado': c.fixado,
                'status': c.status,
                'publicado_em': c.publicado_em or c.criado_em,
                'expira_em': c.expira_em,
                'criado_em': c.criado_em,
                'lido': lido,
            }
            items.append(item_dict)
        return items

    async def create_comunicado(
        self,
        dto: ComunicadoCreate,
        condominio_id: uuid.UUID | None = None,
        autor_id: uuid.UUID | None = None,
    ) -> Comunicado:
        c_id = condominio_id or uuid.uuid4()
        a_id = dto.autor_id or autor_id or uuid.uuid4()
        agora = datetime.now(timezone.utc)
        status_final = 'PUBLICADO' if dto.status == 'RASCUNHO' else dto.status

        comunicado = Comunicado(
            condominio_id=c_id,
            titulo=dto.titulo,
            conteudo=dto.conteudo,
            autor_id=a_id,
            urgente=dto.urgente,
            fixado=dto.fixado,
            status=status_final,
            publicado_em=dto.publicado_em or agora,
            expira_em=dto.expira_em,
        )
        self.db.add(comunicado)
        await self.db.commit()
        await self.db.refresh(comunicado)
        return comunicado

    async def confirmar_leitura(
        self,
        comunicado_id: uuid.UUID,
        pessoa_id: uuid.UUID,
        condominio_id: uuid.UUID | None = None,
    ) -> dict[str, Any]:
        query = select(Comunicado).where(Comunicado.id == comunicado_id)
        if condominio_id:
            query = query.where(Comunicado.condominio_id == condominio_id)
        result = await self.db.execute(query)
        comunicado = result.scalar_one_or_none()
        if not comunicado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='COMUNICADO_NAO_ENCONTRADO',
            )

        # Verificar se já existe leitura
        leitura_q = select(LeituraComunicado).where(
            LeituraComunicado.comunicado_id == comunicado_id,
            LeituraComunicado.pessoa_id == pessoa_id,
        )
        leitura_res = await self.db.execute(leitura_q)
        leitura = leitura_res.scalar_one_or_none()

        if not leitura:
            leitura = LeituraComunicado(
                condominio_id=comunicado.condominio_id,
                comunicado_id=comunicado_id,
                pessoa_id=pessoa_id,
                lido_em=datetime.now(timezone.utc),
            )
            self.db.add(leitura)
            await self.db.commit()
            await self.db.refresh(leitura)

        return {
            'confirmado_em': leitura.lido_em,
            'status': 'CONFIRMADO',
            'comunicado_id': comunicado_id,
            'pessoa_id': pessoa_id,
        }

    async def verificar_urgentes_pendentes(
        self,
        condominio_id: uuid.UUID | None,
        pessoa_id: uuid.UUID,
    ) -> list[dict[str, Any]]:
        comunicados = await self.list_comunicados(
            condominio_id=condominio_id, pessoa_id=pessoa_id
        )
        return [c for c in comunicados if c['urgente'] and not c['lido']]

    async def create_fale_conosco(
        self,
        dto: MensagemFaleConoscoCreate,
        condominio_id: uuid.UUID | None = None,
        remetente_id: uuid.UUID | None = None,
    ) -> MensagemFaleConosco:
        c_id = condominio_id or uuid.uuid4()
        r_id = dto.remetente_id or remetente_id or uuid.uuid4()
        agora = datetime.now(timezone.utc)
        prazo_sla = agora + timedelta(hours=48)

        msg = MensagemFaleConosco(
            condominio_id=c_id,
            remetente_id=r_id,
            destinatario_id=dto.destinatario_id,
            unidade_id=dto.unidade_id,
            assunto=dto.assunto,
            mensagem=dto.mensagem,
            sla_horas=48,
            prazo_sla=prazo_sla,
            status='NOVA_MENSAGEM',
        )
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def list_fale_conosco(
        self,
        condominio_id: uuid.UUID | None = None,
        unidade_id: uuid.UUID | None = None,
        remetente_id: uuid.UUID | None = None,
        is_admin: bool = False,
    ) -> list[MensagemFaleConosco]:
        query = select(MensagemFaleConosco)
        if condominio_id:
            query = query.where(MensagemFaleConosco.condominio_id == condominio_id)
        if not is_admin:
            if unidade_id:
                query = query.where(MensagemFaleConosco.unidade_id == unidade_id)
            elif remetente_id:
                query = query.where(MensagemFaleConosco.remetente_id == remetente_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())


# Aliases de retrocompatibilidade
NoticeService = ComunicadoService

