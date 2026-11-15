import uuid
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Condominio, Inquilino
from .schemas import CondominioInfoUpdate, ConfiguracaoCondominioUpdate


class BrandingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_default_inquilino(self) -> Inquilino:
        res = await self.db.execute(select(Inquilino).limit(1))
        inquilino = res.scalars().first()
        if not inquilino:
            inquilino = Inquilino(
                id=uuid.uuid4(),
                nome='CondoUrban Gestão e Tecnologia SaaS',
                nome_fantasia='CondoUrban',
                documento='12.345.678/0001-90',
                status='ATIVO',
            )
            self.db.add(inquilino)
            await self.db.flush()
        return inquilino

    async def get_or_create_condominio(
        self, condominio_id: uuid.UUID | None = None
    ) -> Condominio:
        inquilino = await self.get_or_create_default_inquilino()

        if condominio_id:
            c = (
                await self.db.execute(
                    select(Condominio).where(Condominio.id == condominio_id)
                )
            ).scalar_one_or_none()
            if c:
                # Se o condomínio tiver inquilino_id inválido ou nulo, repare
                if not c.inquilino_id:
                    c.inquilino_id = inquilino.id
                    await self.db.commit()
                    await self.db.refresh(c)
                return c

        first = (await self.db.execute(select(Condominio))).scalars().first()
        if first:
            if not first.inquilino_id:
                first.inquilino_id = inquilino.id
                await self.db.commit()
                await self.db.refresh(first)
            return first

        # Cria default caso vazio
        c = Condominio(
            id=condominio_id or uuid.uuid4(),
            inquilino_id=inquilino.id,
            nome='Condomínio Residencial Modelo',
            razao_social='Condomínio Residencial Modelo Ltda',
            cnpj='00.000.000/0001-91',
            cidade='São Paulo',
            uf='SP',
            configuracoes={
                'branding': {
                    'nome_fantasia': 'Residencial Modelo',
                    'cor_primaria': '#1E3A8A',
                },
                'regras_operacionais': {
                    'horario_silencio_inicio': '22:00',
                    'horario_silencio_fim': '08:00',
                },
            },
            status='ATIVO',
        )
        self.db.add(c)
        await self.db.commit()
        await self.db.refresh(c)
        return c

    async def update_condominio_info(
        self, condominio_id: uuid.UUID | None, dto: CondominioInfoUpdate
    ) -> Condominio:
        c = await self.get_or_create_condominio(condominio_id)
        if dto.nome is not None:
            c.nome = dto.nome
        if dto.razao_social is not None:
            c.razao_social = dto.razao_social
        if dto.cnpj is not None:
            c.cnpj = dto.cnpj
        if dto.cep is not None:
            c.cep = dto.cep
        if dto.logradouro is not None:
            c.logradouro = dto.logradouro
        if dto.numero is not None:
            c.numero = dto.numero
        if dto.complemento is not None:
            c.complemento = dto.complemento
        if dto.bairro is not None:
            c.bairro = dto.bairro
        if dto.cidade is not None:
            c.cidade = dto.cidade
        if dto.uf is not None:
            c.uf = dto.uf

        await self.db.commit()
        await self.db.refresh(c)
        return c

    async def get_configuracoes(
        self, condominio_id: uuid.UUID | None = None
    ) -> dict:
        c = await self.get_or_create_condominio(condominio_id)
        return c.configuracoes or {}

    async def update_configuracoes(
        self, condominio_id: uuid.UUID | None, dto: ConfiguracaoCondominioUpdate
    ) -> dict:
        c = await self.get_or_create_condominio(condominio_id)
        current = dict(c.configuracoes or {})
        if dto.branding is not None:
            current['branding'] = {**current.get('branding', {}), **dto.branding}
        if dto.regras_operacionais is not None:
            current['regras_operacionais'] = {
                **current.get('regras_operacionais', {}),
                **dto.regras_operacionais,
            }
        if dto.contato_administracao is not None:
            current['contato_administracao'] = {
                **current.get('contato_administracao', {}),
                **dto.contato_administracao,
            }

        c.configuracoes = current
        await self.db.commit()
        await self.db.refresh(c)
        return c.configuracoes

    async def list_condominios(self) -> list[Condominio]:
        result = await self.db.execute(select(Condominio).order_by(Condominio.nome.asc()))
        return list(result.scalars().all())

    async def create_condominio(self, dto: CondominioInfoUpdate) -> Condominio:
        inquilino = await self.get_or_create_default_inquilino()
        c = Condominio(
            id=uuid.uuid4(),
            inquilino_id=inquilino.id,
            nome=dto.nome or 'Novo Condomínio',
            razao_social=dto.razao_social,
            cnpj=dto.cnpj,
            cep=dto.cep,
            logradouro=dto.logradouro,
            numero=dto.numero,
            complemento=dto.complemento,
            bairro=dto.bairro,
            cidade=dto.cidade,
            uf=dto.uf,
            status='ATIVO',
            configuracoes={},
        )
        self.db.add(c)
        await self.db.commit()
        await self.db.refresh(c)
        return c

    async def delete_condominio(self, condominio_id: uuid.UUID) -> dict:
        c = (
            await self.db.execute(select(Condominio).where(Condominio.id == condominio_id))
        ).scalar_one_or_none()
        if not c:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='CONDOMINIO_NAO_ENCONTRADO')

        # Checar se possui blocos
        from app.modules.condominio.blocos_unidades.models import Bloco

        qtd_blocos = (
            await self.db.execute(select(func.count(Bloco.id)).where(Bloco.condominio_id == condominio_id))
        ).scalar_one()
        if qtd_blocos > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'CONDOMINIO_POSSUI_BLOCOS: O condomínio possui {qtd_blocos} bloco(s) cadastrado(s). Exclua os blocos primeiro.',
            )

        await self.db.delete(c)
        await self.db.commit()
        return {'status': 'sucesso', 'mensagem': 'Condomínio excluído com sucesso.'}

