from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_comunicados_crud(async_client: AsyncClient):
    payload = {
        'titulo': 'Manutenção dos elevadores',
        'conteudo': (
            'A manutenção preventiva ocorrerá na próxima terça-feira às 14h.'
        ),
        'urgente': False,
    }
    post_res = await async_client.post(
        '/api/v1/operacional/comunicados', json=payload
    )
    assert post_res.status_code == 201
    comunicado = post_res.json()
    assert comunicado['titulo'] == payload['titulo']
    assert comunicado['urgente'] is False

    get_res = await async_client.get('/api/v1/operacional/comunicados')
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1


@pytest.mark.asyncio
async def test_ocorrencias_crud(async_client: AsyncClient):
    # Criar usuário
    user_res = await async_client.post(
        '/api/v1/identidade/usuarios/registrar',
        json={
            'email': 'morador.ocorrencia@condourban.com.br',
            'nome_completo': 'Lucas Alves',
            'senha': 'senhaSegura123!',
        },
    )
    user_id = user_res.json()['id']

    payload = {
        'usuario_id': user_id,
        'titulo': 'Lâmpada queimada no corredor',
        'descricao': 'Lâmpada do 3º andar do Bloco A está piscando.',
        'categoria': 'manutencao',
        'status': 'aberta',
    }
    post_res = await async_client.post(
        '/api/v1/operacional/ocorrencias', json=payload
    )
    assert post_res.status_code == 201
    ocorrencia = post_res.json()
    assert ocorrencia['usuario_id'] == user_id
    assert ocorrencia['titulo'] == payload['titulo']

    get_res = await async_client.get('/api/v1/operacional/ocorrencias')
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1


@pytest.mark.asyncio
async def test_reservas_crud(async_client: AsyncClient):
    # Criar bloco e unidade
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco F'}
    )
    bloco_id = bloco_res.json()['id']

    unit_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '505', 'andar': '5', 'bloco_id': bloco_id},
    )
    unit_id = unit_res.json()['id']

    # Criar usuário
    user_res = await async_client.post(
        '/api/v1/identidade/usuarios/registrar',
        json={
            'email': 'reserva@condourban.com.br',
            'nome_completo': 'Patricia Souza',
            'senha': 'senhaSegura123!',
        },
    )
    user_id = user_res.json()['id']

    # Criar área comum
    area_res = await async_client.post(
        '/api/v1/condominio/areas-comuns',
        json={
            'nome': 'Churrasqueira 1',
            'capacidade': 20,
            'requer_aprovacao': False,
        },
    )
    area_id = area_res.json()['id']

    inicio = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    fim = (datetime.now(timezone.utc) + timedelta(days=2, hours=4)).isoformat()

    reserva_payload = {
        'area_comum_id': area_id,
        'usuario_id': user_id,
        'unidade_id': unit_id,
        'inicio_em': inicio,
        'fim_em': fim,
        'status': 'solicitada',
    }
    post_res = await async_client.post(
        '/api/v1/operacional/reservas', json=reserva_payload
    )
    assert post_res.status_code == 201
    reserva = post_res.json()
    assert reserva['area_comum_id'] == area_id
    assert reserva['usuario_id'] == user_id
    assert reserva['status'] == 'solicitada'

    get_res = await async_client.get('/api/v1/operacional/reservas')
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1
