from fastapi import APIRouter

router = APIRouter(prefix='/controle-acesso', tags=['Controle de Acesso'])


@router.get('/health')
async def controle_acesso_health() -> dict[str, str]:
    return {'status': 'ok', 'module': 'controle_acesso'}
