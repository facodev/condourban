import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import all models to ensure they are registered with Base.metadata
import app.modules.identidade_cadastro.pessoas.models  # noqa
import app.modules.identidade_cadastro.usuarios.models  # noqa
import app.modules.identidade_cadastro.onboarding.models  # noqa
import app.modules.identidade_cadastro.veiculos_pets.models  # noqa
import app.modules.condominio.branding.models  # noqa
import app.modules.condominio.blocos_unidades.models  # noqa
import app.modules.condominio.vagas.models  # noqa
import app.modules.condominio.estrutura.models  # noqa
import app.modules.condominio.areas_comuns.models  # noqa
import app.modules.controle_acesso.dispositivos.models  # noqa
import app.modules.controle_acesso.credenciais.models  # noqa
import app.modules.controle_acesso.eventos_acesso.models  # noqa
import app.modules.portaria.atendimento.models  # noqa
import app.modules.portaria.encomendas.models  # noqa
import app.modules.reservas.agendamentos.models  # noqa
import app.modules.reservas.vistorias.models  # noqa
import app.modules.comunicacao.mensageria.models  # noqa
import app.modules.comunicacao.ocorrencias.models  # noqa
import app.modules.comunicacao.mural_social.models  # noqa
import app.modules.governanca.assembleias.models  # noqa
import app.modules.governanca.seguranca_auditoria.models  # noqa
import app.modules.financeiro.cobrancas_acordos.models  # noqa
import app.modules.financeiro.despesas_medicoes.models  # noqa
import app.modules.manutencao.chamados_servicos.models  # noqa
import app.modules.manutencao.plano_inventario.models  # noqa

from alembic import context
from app.core.config import settings
from app.core.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration['sqlalchemy.url'] = settings.database_url
    connectable = async_engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
