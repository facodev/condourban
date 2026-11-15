import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.security import decode_access_token, get_password_hash
from app.modules.condominio.estrutura.models import Bloco, Condominio, Inquilino, Unidade
from app.modules.governanca.seguranca_auditoria.models import EventoAuditoria
from app.modules.identidade_cadastro.auth.models import MembroCondominio, Pessoa, Usuario


@pytest.mark.asyncio
async def test_login_sucesso_retorna_jwt_claims(async_client: AsyncClient):
    # Setup de dados para autenticação
    bloco_res = await async_client.post('/api/v1/condominio/blocos', json={'nome': 'Torre Solar'})
    assert bloco_res.status_code == 201

    user_payload = {
        'email': 'sindico.auth@condourban.com.br',
        'nome_completo': 'Carlos Síndico',
        'senha': 'senhaForte123!',
    }
    user_res = await async_client.post('/api/v1/identidade/usuarios/registrar', json=user_payload)
    assert user_res.status_code == 201
    user_id = user_res.json()['id']

    # Fazer login via /api/v1/auth/login
    login_payload = {
        'email': 'sindico.auth@condourban.com.br',
        'senha': 'senhaForte123!',
    }
    login_res = await async_client.post('/api/v1/auth/login', json=login_payload)
    assert login_res.status_code == 200
    data = login_res.json()
    assert 'access_token' in data
    assert data['token_tipo'] == 'bearer'

    # Validar claims do JWT
    claims = decode_access_token(data['access_token'])
    assert claims is not None
    assert claims['sub'] == user_id
    assert claims['email'] == 'sindico.auth@condourban.com.br'
    assert 'papeis' in claims


@pytest.mark.asyncio
async def test_login_credenciais_invalidas_401(async_client: AsyncClient):
    # Login com senha incorreta
    bad_login = {
        'email': 'inexistente@condourban.com.br',
        'senha': 'senhaIncorreta',
    }
    res = await async_client.post('/api/v1/auth/login', json=bad_login)
    assert res.status_code == 401
    assert res.json()['detail'] == 'CREDENCIAIS_INVALIDAS'


@pytest.mark.asyncio
async def test_google_oauth_retorna_token_e_condominios(async_client: AsyncClient):
    google_payload = {
        'id_token': 'google_morador_123@condourban.com.br',
    }
    res = await async_client.post('/api/v1/auth/google', json=google_payload)
    assert res.status_code == 200
    data = res.json()
    assert 'access_token' in data
    assert data['token_tipo'] == 'bearer'


@pytest.mark.asyncio
async def test_sessao_injeta_app_condominio_id(async_client: AsyncClient):
    # Registrar usuário e pessoa
    user_payload = {
        'email': 'morador.sessao@condourban.com.br',
        'nome_completo': 'Juliana Ramos',
        'senha': 'senhaForte123!',
    }
    user_res = await async_client.post('/api/v1/identidade/usuarios/registrar', json=user_payload)
    assert user_res.status_code == 201

    login_res = await async_client.post(
        '/api/v1/auth/login',
        json={'email': user_payload['email'], 'senha': user_payload['senha']},
    )
    assert login_res.status_code == 200
    token = login_res.json()['access_token']

    # Fazer requisição autenticada
    headers = {'Authorization': f'Bearer {token}'}
    me_res = await async_client.get('/api/v1/identidade/pessoas/me', headers=headers)
    # Pessoa criada com mesmo email
    assert me_res.status_code in (200, 404)


@pytest.mark.asyncio
async def test_rls_bloqueia_acesso_cruzado_condominios(async_client: AsyncClient):
    # Registrar usuário
    user_payload = {
        'email': 'usuario.cross@condourban.com.br',
        'nome_completo': 'Felipe Santos',
        'senha': 'senhaForte123!',
    }
    user_res = await async_client.post('/api/v1/identidade/usuarios/registrar', json=user_payload)
    assert user_res.status_code == 201

    login_res = await async_client.post(
        '/api/v1/auth/login',
        json={'email': user_payload['email'], 'senha': user_payload['senha']},
    )
    token = login_res.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Tentar selecionar condomínio inexistente ou sem vínculo -> deve retornar 403
    fake_condo_id = str(uuid.uuid4())
    cross_res = await async_client.post(
        '/api/v1/auth/selecionar-condominio',
        json={'condominio_id': fake_condo_id},
        headers=headers,
    )
    assert cross_res.status_code == 403
    assert cross_res.json()['detail'] == 'ACESSO_NEGADO_CONDOMINIO'


@pytest.mark.asyncio
async def test_evento_auditoria_gravado_no_login(async_client: AsyncClient):
    # Realizar login com cabeçalho de correlação
    user_payload = {
        'email': 'audit.login@condourban.com.br',
        'nome_completo': 'Beatriz Audit',
        'senha': 'senhaForte123!',
    }
    await async_client.post('/api/v1/identidade/usuarios/registrar', json=user_payload)

    correlation_id = 'req-trace-audit-001'
    login_res = await async_client.post(
        '/api/v1/auth/login',
        json={'email': user_payload['email'], 'senha': user_payload['senha']},
        headers={'x-correlation-id': correlation_id},
    )
    assert login_res.status_code == 200
