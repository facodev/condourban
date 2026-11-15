from datetime import datetime, timedelta, timezone
from typing import Any
import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Documento, PastaDocumento
from .schemas import DocumentoCreate, PastaDocumentoCreate


class DocumentosService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pasta(
        self,
        dto: PastaDocumentoCreate,
        condominio_id: uuid.UUID | None = None,
    ) -> PastaDocumento:
        c_id = condominio_id or uuid.uuid4()
        pasta = PastaDocumento(
            condominio_id=c_id,
            pasta_pai_id=dto.pasta_pai_id,
            nome=dto.nome,
            visibilidade=dto.visibilidade or 'ADMINISTRADORES',
        )
        self.db.add(pasta)
        await self.db.commit()
        await self.db.refresh(pasta)
        return pasta

    async def list_pastas(
        self,
        condominio_id: uuid.UUID | None = None,
    ) -> list[PastaDocumento]:
        query = select(PastaDocumento)
        if condominio_id:
            query = query.where(PastaDocumento.condominio_id == condominio_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_documento(
        self,
        dto: DocumentoCreate,
        condominio_id: uuid.UUID | None = None,
        enviado_por: uuid.UUID | None = None,
    ) -> Documento:
        c_id = condominio_id or uuid.uuid4()
        doc = Documento(
            condominio_id=c_id,
            pasta_id=dto.pasta_id,
            nome=dto.nome,
            chave_armazenamento=dto.chave_armazenamento,
            tipo_mime=dto.tipo_mime,
            tamanho_bytes=dto.tamanho_bytes,
            hash_arquivo=dto.hash_arquivo,
            versao=dto.versao or 1,
            vencimento_em=dto.vencimento_em,
            enviado_por=enviado_por,
        )
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def list_documentos(
        self,
        condominio_id: uuid.UUID | None = None,
        pasta_id: uuid.UUID | None = None,
    ) -> list[Documento]:
        query = select(Documento).options(selectinload(Documento.pasta))
        if condominio_id:
            query = query.where(Documento.condominio_id == condominio_id)
        if pasta_id:
            query = query.where(Documento.pasta_id == pasta_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_download_info(
        self,
        documento_id: uuid.UUID,
        is_admin: bool = False,
    ) -> dict[str, str]:
        query = (
            select(Documento)
            .options(selectinload(Documento.pasta))
            .where(Documento.id == documento_id)
        )
        result = await self.db.execute(query)
        doc = result.scalar_one_or_none()
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='DOCUMENTO_NAO_ENCONTRADO',
            )

        if doc.pasta and doc.pasta.visibilidade == 'ADMINISTRADORES' and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='ACESSO_RESTRITO',
            )

        return {
            'url': f'https://storage.condourban.com.br/documentos/{doc.chave_armazenamento}',
            'nome': doc.nome,
        }

    async def list_alertas_vencimento(
        self,
        condominio_id: uuid.UUID | None = None,
    ) -> list[dict[str, Any]]:
        query = select(Documento).where(Documento.vencimento_em.isnot(None))
        if condominio_id:
            query = query.where(Documento.condominio_id == condominio_id)
        result = await self.db.execute(query)
        documentos = list(result.scalars().all())

        agora = datetime.now(timezone.utc)
        limite_30_dias = agora + timedelta(days=30)
        alertas = []

        for doc in documentos:
            venc = doc.vencimento_em
            if venc.tzinfo is None:
                venc = venc.replace(tzinfo=timezone.utc)
            if venc <= limite_30_dias:
                delta = venc - agora
                dias = max(0, delta.days)
                alertas.append({
                    'documento_id': doc.id,
                    'nome': doc.nome,
                    'vencimento_em': doc.vencimento_em,
                    'dias_restantes': dias,
                })
        return alertas
