from datetime import datetime, timedelta, timezone
import uuid
import pytest
from httpx import AsyncClient

from app.core.security import create_access_token


def _make_token(user_id: str, papeis: list[str], condominio_id: str | None = None) -> str:
    return create_access_token(
        subject=user_id,
        extra_claims={
            'papeis': papeis,
            'condominio_id': condominio_id or str(uuid.uuid4()),
            'email': f'user_{user_id[:8]}@condourban.com.br',
        },
    )


@pytest.mark.asyncio
async def test_upload_documento_metadados_201(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(sindico_id, ['SINDICO'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'nome': 'Regimento Interno Consolidado 2026.pdf',
        'chave_armazenamento': 'docs/2026/regimento_interno.pdf',
        'tipo_mime': 'application/pdf',
        'tamanho_bytes': 2048500,
        'hash_arquivo': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    }
    res = await async_client.post('/api/v1/governanca/documentos', json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data['id'] is not None
    assert data['nome'] == payload['nome']
    assert data['chave_armazenamento'] == payload['chave_armazenamento']


@pytest.mark.asyncio
async def test_download_documento_administradores_permitido(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(sindico_id, ['SINDICO'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    # 1. Criar pasta com visibilidade ADMINISTRADORES
    pasta_res = await async_client.post(
        '/api/v1/governanca/documentos/pastas',
        json={'nome': 'Contratos e Pareceres Jurídicos', 'visibilidade': 'ADMINISTRADORES'},
        headers=headers,
    )
    assert pasta_res.status_code == 201
    pasta_id = pasta_res.json()['id']

    # 2. Criar documento dentro da pasta restrita
    doc_payload = {
        'pasta_id': pasta_id,
        'nome': 'Contrato Administradora 2026-2028.pdf',
        'chave_armazenamento': 'docs/contratos/adm_2026.pdf',
        'tipo_mime': 'application/pdf',
    }
    doc_res = await async_client.post('/api/v1/governanca/documentos', json=doc_payload, headers=headers)
    assert doc_res.status_code == 201
    doc_id = doc_res.json()['id']

    # 3. Síndico solicita download -> 200
    down_res = await async_client.get(f'/api/v1/governanca/documentos/{doc_id}/download', headers=headers)
    assert down_res.status_code == 200
    assert 'url' in down_res.json()
    assert down_res.json()['nome'] == doc_payload['nome']


@pytest.mark.asyncio
async def test_morador_download_documento_restrito_retorna_403(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    morador_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())

    sindico_token = _make_token(sindico_id, ['SINDICO'], condo_id)
    morador_token = _make_token(morador_id, ['MORADOR'], condo_id)

    # 1. Gestão cria pasta restrita e documento confidencial
    pasta_res = await async_client.post(
        '/api/v1/governanca/documentos/pastas',
        json={'nome': 'Processos Trabalhistas e Sigilo', 'visibilidade': 'ADMINISTRADORES'},
        headers={'Authorization': f'Bearer {sindico_token}'},
    )
    assert pasta_res.status_code == 201
    pasta_id = pasta_res.json()['id']

    doc_res = await async_client.post(
        '/api/v1/governanca/documentos',
        json={'pasta_id': pasta_id, 'nome': 'Parecer_Trabalhista.pdf', 'chave_armazenamento': 'docs/sigilo/trabalhista.pdf'},
        headers={'Authorization': f'Bearer {sindico_token}'},
    )
    assert doc_res.status_code == 201
    doc_id = doc_res.json()['id']

    # 2. Morador tenta efetuar download -> 403 ACESSO_RESTRITO
    morador_down = await async_client.get(
        f'/api/v1/governanca/documentos/{doc_id}/download',
        headers={'Authorization': f'Bearer {morador_token}'},
    )
    assert morador_down.status_code == 403
    assert morador_down.json()['detail'] == 'ACESSO_RESTRITO'


@pytest.mark.asyncio
async def test_alerta_vencimento_documento_seguranca_30_dias(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(sindico_id, ['SINDICO'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    # Documento de conformidade predial vencendo em 18 dias (< 30 dias)
    vencimento_proximo = (datetime.now(timezone.utc) + timedelta(days=18)).isoformat()
    doc_avcb = {
        'nome': 'Auto de Vistoria do Corpo de Bombeiros (AVCB).pdf',
        'chave_armazenamento': 'docs/seguranca/avcb_2026.pdf',
        'vencimento_em': vencimento_proximo,
    }
    res_avcb = await async_client.post('/api/v1/governanca/documentos', json=doc_avcb, headers=headers)
    assert res_avcb.status_code == 201
    avcb_id = res_avcb.json()['id']

    # Documento com vencimento distante (90 dias)
    vencimento_longe = (datetime.now(timezone.utc) + timedelta(days=90)).isoformat()
    doc_longe = {
        'nome': 'Apólice de Seguro Predial 2027.pdf',
        'chave_armazenamento': 'docs/seguranca/apolice_2027.pdf',
        'vencimento_em': vencimento_longe,
    }
    await async_client.post('/api/v1/governanca/documentos', json=doc_longe, headers=headers)

    # Consulta painel de alertas de vencimento da gestão
    alertas_res = await async_client.get(
        f'/api/v1/governanca/documentos/alertas-vencimento?condominio_id={condo_id}',
        headers=headers,
    )
    assert alertas_res.status_code == 200
    alertas = alertas_res.json()
    assert len(alertas) >= 1
    avcb_alerta = next((a for a in alertas if a['documento_id'] == avcb_id), None)
    assert avcb_alerta is not None
    assert avcb_alerta['dias_restantes'] <= 30
