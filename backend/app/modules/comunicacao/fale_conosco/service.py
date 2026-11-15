from datetime import datetime, timedelta, timezone
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import MensagemFaleConosco
from .schemas import MensagemFaleConoscoCreate


class FaleConoscoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_mensagem(
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

    async def list_mensagens(
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
