import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_visitantes_crud(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    headers = {'X-Condominio-Id': condo_id}

    # Criar bloco e unidade para vincular o visitante
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco C'}, headers=headers
    )
    bloco_id = bloco_res.json()['id']

    unit_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '202', 'andar': '2', 'bloco_id': bloco_id},
        headers=headers,
    )
    unit_id = unit_res.json()['id']

    # Criar visitante
    visitor_payload = {
        'nome_completo': 'Carlos da Silva',
        'documento': '12345678900',
        'unidade_id': unit_id,
        'status': 'autorizado',
    }
    post_res = await async_client.post(
        '/api/v1/acesso/visitantes', json=visitor_payload, headers=headers
    )
    assert post_res.status_code == 201
    vis = post_res.json()
    assert vis['nome_completo'] == 'Carlos da Silva'
    assert vis['documento'] == '12345678900'
    assert vis['unidade_id'] == unit_id

    # Listar visitantes
    get_res = await async_client.get('/api/v1/acesso/visitantes', headers=headers)
    assert get_res.status_code == 200
    visitantes = get_res.json()
    assert len(visitantes) == 1


@pytest.mark.asyncio
async def test_encomendas_crud(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    headers = {'X-Condominio-Id': condo_id}

    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco D'}, headers=headers
    )
    bloco_id = bloco_res.json()['id']

    unit_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '303', 'andar': '3', 'bloco_id': bloco_id},
        headers=headers,
    )
    unit_id = unit_res.json()['id']

    delivery_payload = {
        'codigo_rastreio': 'BR123456789',
        'unidade_id': unit_id,
        'descricao': 'Pacote Mercado Livre',
        'status': 'recebida',
    }
    post_res = await async_client.post(
        '/api/v1/acesso/encomendas', json=delivery_payload, headers=headers
    )
    assert post_res.status_code == 201
    deliv = post_res.json()
    assert deliv['codigo_rastreio'] == 'BR123456789'
    assert deliv['unidade_id'] == unit_id

    get_res = await async_client.get('/api/v1/acesso/encomendas', headers=headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1
