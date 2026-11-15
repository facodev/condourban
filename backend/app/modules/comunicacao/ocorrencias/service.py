from datetime import datetime, timezone
from typing import Any
import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import HistoricoOcorrencia, Ocorrencia
from .schemas import HistoricoOcorrenciaCreate, OcorrenciaCreate

STATUS_VALIDOS = {'ABERTA', 'EM_ANALISE', 'EM_ANDAMENTO', 'RESOLVIDA', 'FECHADA', 'CANCELADA'}


class OcorrenciaService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_ocorrencias(
        self,
        condominio_id: uuid.UUID | None = None,
        current_user_id: uuid.UUID | None = None,
        is_admin: bool = False,
    ) -> list[dict[str, Any]]:
        query = select(Ocorrencia).options(selectinload(Ocorrencia.historico))
        if condominio_id:
            query = query.where(Ocorrencia.condominio_id == condominio_id)
        result = await self.db.execute(query)
        ocorrencias = list(result.scalars().all())

        items = []
        for o in ocorrencias:
            o_dict = {
                'id': o.id,
                'condominio_id': o.condominio_id,
                'unidade_id': o.unidade_id,
                'registrada_por': o.registrada_por,
                'origem': o.origem,
                'categoria': o.categoria,
                'titulo': o.titulo,
                'descricao': o.descricao,
                'prioridade': o.prioridade,
                'status': o.status,
                'sigilosa': o.sigilosa,
                'responsavel_id': o.responsavel_id,
                'criada_em': o.criada_em,
                'resolvida_em': o.resolvida_em,
                'historico': o.historico,
                'usuario_id': o.registrada_por,
                'criado_em': o.criada_em,
            }
            # Máscara de sigilo anti-retaliação para terceiros
            if o.sigilosa and not is_admin:
                if not current_user_id or str(o.registrada_por) != str(current_user_id):
                    o_dict['registrada_por'] = None
                    o_dict['unidade_id'] = None
                    o_dict['usuario_id'] = None
            items.append(o_dict)
        return items

    async def get_ocorrencia(
        self,
        ocorrencia_id: uuid.UUID,
        current_user_id: uuid.UUID | None = None,
        is_admin: bool = False,
    ) -> dict[str, Any]:
        query = (
            select(Ocorrencia)
            .options(selectinload(Ocorrencia.historico))
            .where(Ocorrencia.id == ocorrencia_id)
        )
        result = await self.db.execute(query)
        o = result.scalar_one_or_none()
        if not o:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='OCORRENCIA_NAO_ENCONTRADA',
            )

        if o.sigilosa and not is_admin:
            if not current_user_id or str(o.registrada_por) != str(current_user_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='OCORRENCIA_NAO_ENCONTRADA',
                )

        return {
            'id': o.id,
            'condominio_id': o.condominio_id,
            'unidade_id': o.unidade_id,
            'registrada_por': o.registrada_por,
            'origem': o.origem,
            'categoria': o.categoria,
            'titulo': o.titulo,
            'descricao': o.descricao,
            'prioridade': o.prioridade,
            'status': o.status,
            'sigilosa': o.sigilosa,
            'responsavel_id': o.responsavel_id,
            'criada_em': o.criada_em,
            'resolvida_em': o.resolvida_em,
            'historico': o.historico,
            'usuario_id': o.registrada_por,
            'criado_em': o.criada_em,
        }

    async def create_ocorrencia(
        self,
        dto: OcorrenciaCreate,
        condominio_id: uuid.UUID | None = None,
        registrada_por: uuid.UUID | None = None,
        origem: str | None = None,
    ) -> Ocorrencia:
        c_id = condominio_id or uuid.uuid4()
        r_id = dto.registrada_por or dto.usuario_id or registrada_por or uuid.uuid4()
        origem_final = origem or dto.origem or 'MORADOR'

        ocorrencia = Ocorrencia(
            condominio_id=c_id,
            unidade_id=dto.unidade_id,
            registrada_por=r_id,
            origem=origem_final,
            categoria=dto.categoria,
            titulo=dto.titulo,
            descricao=dto.descricao,
            prioridade=dto.prioridade or 'NORMAL',
            status='ABERTA',
            sigilosa=dto.sigilosa or False,
            responsavel_id=dto.responsavel_id,
        )
        self.db.add(ocorrencia)
        await self.db.commit()
        await self.db.refresh(ocorrencia)
        return ocorrencia

    async def update_status(
        self,
        ocorrencia_id: uuid.UUID,
        novo_status: str,
        mensagem: str | None = None,
        autor_id: uuid.UUID | None = None,
    ) -> Ocorrencia:
        query = (
            select(Ocorrencia)
            .options(selectinload(Ocorrencia.historico))
            .where(Ocorrencia.id == ocorrencia_id)
        )
        result = await self.db.execute(query)
        ocorrencia = result.scalar_one_or_none()
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='OCORRENCIA_NAO_ENCONTRADA',
            )

        status_upper = novo_status.upper()
        if status_upper not in STATUS_VALIDOS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='STATUS_INVALIDO',
            )

        ocorrencia.status = status_upper
        if status_upper in ('RESOLVIDA', 'FECHADA'):
            ocorrencia.resolvida_em = datetime.now(timezone.utc)

        # Gravar histórico imutável
        a_id = autor_id or ocorrencia.registrada_por
        historico = HistoricoOcorrencia(
            ocorrencia_id=ocorrencia.id,
            autor_id=a_id,
            tipo='MUDANCA_STATUS',
            mensagem=mensagem or f'Status alterado para {status_upper}',
        )
        self.db.add(historico)
        await self.db.commit()
        await self.db.refresh(ocorrencia)
        return ocorrencia

    async def add_evento(
        self,
        ocorrencia_id: uuid.UUID,
        dto: HistoricoOcorrenciaCreate,
        autor_id: uuid.UUID | None = None,
    ) -> HistoricoOcorrencia:
        query = select(Ocorrencia).where(Ocorrencia.id == ocorrencia_id)
        result = await self.db.execute(query)
        ocorrencia = result.scalar_one_or_none()
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='OCORRENCIA_NAO_ENCONTRADA',
            )

        a_id = dto.autor_id or autor_id or uuid.uuid4()
        evento = HistoricoOcorrencia(
            ocorrencia_id=ocorrencia.id,
            autor_id=a_id,
            tipo=dto.tipo or 'COMENTARIO',
            mensagem=dto.mensagem,
        )
        self.db.add(evento)
        await self.db.commit()
        await self.db.refresh(evento)
        return evento


# Aliases de retrocompatibilidade
OccurrenceService = OcorrenciaService

