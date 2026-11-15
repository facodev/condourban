import uuid

import pytest
from httpx import AsyncClient

from app.core.security import create_access_token


def _token(
    *,
    papeis: list[str],
    condominio_id: str | None = None,
    pessoa_id: str | None = None,
    unidade_ids: list[str] | None = None,
    user_id: str | None = None,
) -> str:
    condo = condominio_id or str(uuid.uuid4())
    return create_access_token(
        subject=user_id or str(uuid.uuid4()),
        extra_claims={
            'papeis': papeis,
            'condominio_id': condo,
            'email': f'{papeis[0].lower()}@test.condourban.com',
            'pessoa_id': pessoa_id,
            'unidade_ids': unidade_ids or [],
        },
    )


def _headers(token: str, condominio_id: str | None = None) -> dict[str, str]:
    h = {'Authorization': f'Bearer {token}'}
    if condominio_id:
        h['X-Condominio-Id'] = condominio_id
    return h


@pytest.mark.asyncio
async def test_encomendas_create_list_baixa_por_encomendas(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    unidade_id = str(uuid.uuid4())
    token = _token(papeis=['ENCOMENDAS'], condominio_id=condo_id)
    headers = _headers(token, condo_id)

    create_res = await async_client.post(
        '/api/v1/portaria/encomendas',
        json={
            'unidade_id': unidade_id,
            'transportadora': 'Mercado Livre',
            'codigo_rastreio': 'ML-TEST-001',
            'descricao': 'Caixa pequena',
        },
        headers=headers,
    )
    assert create_res.status_code == 201, create_res.text
    data = create_res.json()
    assert data['status'] == 'RECEBIDA'
    assert data['codigo_retirada'] is not None
    assert len(data['codigo_retirada']) == 4
    assert data['codigo_retirada'].isdigit()
    pin = data['codigo_retirada']
    encomenda_id = data['id']

    list_res = await async_client.get('/api/v1/portaria/encomendas', headers=headers)
    assert list_res.status_code == 200
    lista = list_res.json()
    assert any(item['id'] == encomenda_id for item in lista)

    baixa_res = await async_client.post(
        f'/api/v1/portaria/encomendas/{encomenda_id}/baixa',
        json={'codigo_retirada': pin},
        headers=headers,
    )
    assert baixa_res.status_code == 200, baixa_res.text
    entregue = baixa_res.json()
    assert entregue['status'] == 'ENTREGUE'
    assert entregue['retirada_em'] is not None


@pytest.mark.asyncio
async def test_baixa_pin_invalido_retorna_400(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    token = _token(papeis=['ENCOMENDAS'], condominio_id=condo_id)
    headers = _headers(token, condo_id)

    create_res = await async_client.post(
        '/api/v1/portaria/encomendas',
        json={'unidade_id': str(uuid.uuid4()), 'transportadora': 'Amazon'},
        headers=headers,
    )
    assert create_res.status_code == 201
    encomenda_id = create_res.json()['id']

    bad = await async_client.post(
        f'/api/v1/portaria/encomendas/{encomenda_id}/baixa',
        json={'codigo_retirada': '0000'},
        headers=headers,
    )
    # PIN gerado pode coincidir com 0000 raramente; força diferença se necessário
    if bad.status_code == 200:
        # recria
        create_res = await async_client.post(
            '/api/v1/portaria/encomendas',
            json={'unidade_id': str(uuid.uuid4()), 'transportadora': 'Amazon'},
            headers=headers,
        )
        encomenda_id = create_res.json()['id']
        pin = create_res.json()['codigo_retirada']
        wrong = '1111' if pin != '1111' else '2222'
        bad = await async_client.post(
            f'/api/v1/portaria/encomendas/{encomenda_id}/baixa',
            json={'codigo_retirada': wrong},
            headers=headers,
        )
    assert bad.status_code == 400
    assert bad.json()['detail'] == 'PIN_INVALIDO'


@pytest.mark.asyncio
async def test_post_encomenda_morador_e_portaria_retorna_403(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    payload = {'unidade_id': str(uuid.uuid4()), 'transportadora': 'Correios'}

    for papel in ('MORADOR', 'PORTARIA', 'PORTEIRO'):
        token = _token(papeis=[papel], condominio_id=condo_id)
        res = await async_client.post(
            '/api/v1/portaria/encomendas',
            json=payload,
            headers=_headers(token, condo_id),
        )
        assert res.status_code == 403, papel


@pytest.mark.asyncio
async def test_morador_lista_somente_propria_unidade(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    unidade_a = str(uuid.uuid4())
    unidade_b = str(uuid.uuid4())

    op_token = _token(papeis=['ENCOMENDAS'], condominio_id=condo_id)
    op_headers = _headers(op_token, condo_id)

    a_res = await async_client.post(
        '/api/v1/portaria/encomendas',
        json={'unidade_id': unidade_a, 'transportadora': 'ML'},
        headers=op_headers,
    )
    b_res = await async_client.post(
        '/api/v1/portaria/encomendas',
        json={'unidade_id': unidade_b, 'transportadora': 'Amazon'},
        headers=op_headers,
    )
    assert a_res.status_code == 201
    assert b_res.status_code == 201
    id_a = a_res.json()['id']
    id_b = b_res.json()['id']

    morador_token = _token(
        papeis=['MORADOR'],
        condominio_id=condo_id,
        unidade_ids=[unidade_a],
    )
    list_res = await async_client.get(
        '/api/v1/portaria/encomendas',
        headers=_headers(morador_token, condo_id),
    )
    assert list_res.status_code == 200
    ids = {item['id'] for item in list_res.json()}
    assert id_a in ids
    assert id_b not in ids


@pytest.mark.asyncio
async def test_visitantes_portaria_cria_e_lista(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    token = _token(papeis=['PORTARIA'], condominio_id=condo_id)
    headers = _headers(token, condo_id)

    create_res = await async_client.post(
        '/api/v1/portaria/visitantes',
        json={
            'nome_completo': 'Visitante Teste',
            'documento': '123.456.789-00',
            'unidade_id': str(uuid.uuid4()),
            'observacao': 'Chegada na guarita',
        },
        headers=headers,
    )
    assert create_res.status_code == 201, create_res.text
    data = create_res.json()
    assert data['id'] is not None
    assert data['status']

    list_res = await async_client.get('/api/v1/portaria/visitantes', headers=headers)
    assert list_res.status_code == 200
    assert any(item['id'] == data['id'] for item in list_res.json())


@pytest.mark.asyncio
async def test_post_visitante_morador_e_encomendas_retorna_403(async_client: AsyncClient):
    condo_id = str(uuid.uuid4())
    payload = {'nome_completo': 'Sem Acesso', 'documento': '000'}

    for papel in ('MORADOR', 'ENCOMENDAS'):
        token = _token(papeis=[papel], condominio_id=condo_id)
        res = await async_client.post(
            '/api/v1/portaria/visitantes',
            json=payload,
            headers=_headers(token, condo_id),
        )
        assert res.status_code == 403, papel


@pytest.mark.asyncio
async def test_portaria_sem_token_retorna_401(async_client: AsyncClient):
    from app.core.dependencies import get_current_user
    from app.main import app

    # Remove override de gestão padrão — exige Bearer real (C14)
    app.dependency_overrides.pop(get_current_user, None)
    try:
        for path, method in (
            ('/api/v1/portaria/encomendas', 'get'),
            ('/api/v1/portaria/encomendas', 'post'),
            ('/api/v1/portaria/visitantes', 'get'),
            ('/api/v1/portaria/visitantes', 'post'),
        ):
            if method == 'get':
                res = await async_client.get(path)
            else:
                res = await async_client.post(path, json={})
            assert res.status_code == 401, path
    finally:
        # Restaurado no teardown do fixture async_client
        pass

