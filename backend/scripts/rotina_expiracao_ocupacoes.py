"""Script CLI para execução da rotina diária de expiração de ocupações.

Varre o banco de dados inativando ocupações cujo fim_em < now() e
aplica o cascade automático para dependentes órfãos.
Pode ser agendado via Cron do Linux, Celery Beat, Task Scheduler ou Kubernetes CronJob.

Uso:
    python -m scripts.rotina_expiracao_ocupacoes [--condominio-id <UUID>]
"""

import argparse
import asyncio
import logging
import sys
import uuid

from app.core.database import async_session_maker
from app.modules.identidade_cadastro.usuarios.service import OcupacaoUnidadeService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger('rotina_expiracao_ocupacoes')


async def main(condominio_id: uuid.UUID | None = None) -> None:
    logger.info('Iniciando rotina de expiração de vínculos de ocupação...')
    if condominio_id:
        logger.info(f'Filtrando por condomínio: {condominio_id}')

    async with async_session_maker() as session:
        service = OcupacaoUnidadeService(session)
        resultado = await service.executar_rotina_expiracao(condominio_id=condominio_id)

    logger.info(
        f'Rotina concluída com sucesso! '
        f'Ocupações inativadas: {resultado.ocupacoes_inativadas} | '
        f'Dependentes inativados: {resultado.dependentes_inativados}'
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Rotina diária de expiração de ocupações e corte de acessos.'
    )
    parser.add_argument(
        '--condominio-id',
        type=uuid.UUID,
        default=None,
        help='ID do condomínio opcional para filtrar a varredura.',
    )
    args = parser.parse_args()

    asyncio.run(main(condominio_id=args.condominio_id))
