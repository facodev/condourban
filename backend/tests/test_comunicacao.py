from datetime import datetime, timezone
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
async def test_publicar_comunicado_retorna_201(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(sindico_id, ['SINDICO'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'titulo': 'Interrupção programada de fornecimento de água',
        'conteudo': 'O abastecimento de água será interrompido para limpeza da caixa d água na quinta-feira.',
        'urgente': False,
        'fixado': True,
    }
    res = await async_client.post('/api/v1/comunicacao/comunicados', json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data['id'] is not None
    assert data['titulo'] == payload['titulo']
    assert data['status'] == 'PUBLICADO'
    assert data['publicado_em'] is not None


@pytest.mark.asyncio
async def test_comunicado_urgente_bloqueia_navegacao(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    morador_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())

    sindico_token = _make_token(sindico_id, ['SINDICO'], condo_id)
    morador_token = _make_token(morador_id, ['MORADOR'], condo_id)

    # 1. Síndico publica aviso com urgente = True
    payload = {
        'titulo': 'ALERTA URGENTE: Vazamento de gás na Torre Central',
        'conteudo': 'Evacuação imediata das áreas de subsolo e desligamento de aquecedores.',
        'urgente': True,
    }
    pub_res = await async_client.post(
        '/api/v1/comunicacao/comunicados',
        json=payload,
        headers={'Authorization': f'Bearer {sindico_token}'},
    )
    assert pub_res.status_code == 201
    comunicado_id = pub_res.json()['id']

    # 2. Morador consulta comunicados urgentes pendentes de leitura
    check_res = await async_client.get(
        '/api/v1/comunicacao/comunicados/urgentes-pendentes',
        headers={'Authorization': f'Bearer {morador_token}'},
    )
    assert check_res.status_code == 200
    pendentes = check_res.json()
    assert len(pendentes) >= 1
    assert any(p['id'] == comunicado_id for p in pendentes)

    # 3. Morador confirma leitura
    conf_res = await async_client.post(
        f'/api/v1/comunicacao/comunicados/{comunicado_id}/confirmar-leitura',
        headers={'Authorization': f'Bearer {morador_token}'},
    )
    assert conf_res.status_code == 200

    # 4. Não há mais comunicados urgentes bloqueantes pendentes
    recheck_res = await async_client.get(
        '/api/v1/comunicacao/comunicados/urgentes-pendentes',
        headers={'Authorization': f'Bearer {morador_token}'},
    )
    assert recheck_res.status_code == 200
    novos_pendentes = [p for p in recheck_res.json() if p['id'] == comunicado_id]
    assert len(novos_pendentes) == 0


@pytest.mark.asyncio
async def test_confirmar_leitura_grava_ciencia_200(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    morador_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())

    sindico_token = _make_token(sindico_id, ['SINDICO'], condo_id)
    morador_token = _make_token(morador_id, ['MORADOR'], condo_id)

    pub_res = await async_client.post(
        '/api/v1/comunicacao/comunicados',
        json={'titulo': 'Edital de Convocação de Assembleia Ordinária', 'conteudo': 'Pauta e datas.'},
        headers={'Authorization': f'Bearer {sindico_token}'},
    )
    assert pub_res.status_code == 201
    comunicado_id = pub_res.json()['id']

    # Confirmar leitura
    read_res = await async_client.post(
        f'/api/v1/comunicacao/comunicados/{comunicado_id}/confirmar-leitura',
        headers={'Authorization': f'Bearer {morador_token}'},
    )
    assert read_res.status_code == 200
    data = read_res.json()
    assert data['status'] == 'CONFIRMADO'
    assert data['confirmado_em'] is not None
    assert data['comunicado_id'] == comunicado_id


@pytest.mark.asyncio
async def test_morador_publicar_comunicado_retorna_403(async_client: AsyncClient):
    morador_id = str(uuid.uuid4())
    token = _make_token(morador_id, ['MORADOR'])
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'titulo': 'Tentativa de aviso oficial por morador',
        'conteudo': 'Morador tentando publicar canal oficial.',
    }
    res = await async_client.post('/api/v1/comunicacao/comunicados', json=payload, headers=headers)
    assert res.status_code == 403
    assert res.json()['detail'] == 'PERMISSAO_NEGADA'


@pytest.mark.asyncio
async def test_criar_ocorrencia_morador_origem_morador(async_client: AsyncClient):
    morador_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(morador_id, ['MORADOR'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'titulo': 'Barulho excessivo acima do horário permitido',
        'descricao': 'Som alto e instrumentos musicais após as 22h na unidade vizinha.',
        'categoria': 'barulho',
        'sigilosa': False,
    }
    res = await async_client.post('/api/v1/comunicacao/ocorrencias', json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data['id'] is not None
    assert data['origem'] == 'MORADOR'
    assert data['status'] == 'ABERTA'


@pytest.mark.asyncio
async def test_criar_ocorrencia_guarita_origem_portaria(async_client: AsyncClient):
    porteiro_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(porteiro_id, ['PORTEIRO'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'titulo': 'Registro da Guarita: Veículo bloqueando rampa de acessibilidade',
        'descricao': 'Veículo estacionado sobre faixa de pedestres no portão principal.',
        'origem': 'PORTARIA',
    }
    res = await async_client.post('/api/v1/comunicacao/ocorrencias', json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data['origem'] == 'PORTARIA'


@pytest.mark.asyncio
async def test_ocorrencia_sigilosa_oculta_dados_autor(async_client: AsyncClient):
    morador_a_id = str(uuid.uuid4())
    morador_b_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())

    token_a = _make_token(morador_a_id, ['MORADOR'], condo_id)
    token_b = _make_token(morador_b_id, ['MORADOR'], condo_id)

    # Morador A abre ocorrência sigilosa
    payload = {
        'titulo': 'Denúncia sigilosa de animal sem coleira em área infantil',
        'descricao': 'Cachorro de grande porte solto no parquinho.',
        'sigilosa': True,
    }
    res_a = await async_client.post(
        '/api/v1/comunicacao/ocorrencias',
        json=payload,
        headers={'Authorization': f'Bearer {token_a}'},
    )
    assert res_a.status_code == 201
    ocorr_id = res_a.json()['id']

    # Morador B lista ocorrências e dados do autor são omitidos para proteger anti-retaliação
    res_b = await async_client.get(
        '/api/v1/comunicacao/ocorrencias',
        headers={'Authorization': f'Bearer {token_b}'},
    )
    assert res_b.status_code == 200
    items = res_b.json()
    target_item = next((o for o in items if o['id'] == ocorr_id), None)
    assert target_item is not None
    assert target_item['registrada_por'] is None
    assert target_item['unidade_id'] is None


@pytest.mark.asyncio
async def test_tramitar_status_ocorrencia_grava_historico(async_client: AsyncClient):
    sindico_id = str(uuid.uuid4())
    morador_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())

    morador_token = _make_token(morador_id, ['MORADOR'], condo_id)
    sindico_token = _make_token(sindico_id, ['SINDICO'], condo_id)

    # Criar ocorrência
    create_res = await async_client.post(
        '/api/v1/comunicacao/ocorrencias',
        json={'titulo': 'Infiltração no teto da garagem', 'descricao': 'Goteira constante.'},
        headers={'Authorization': f'Bearer {morador_token}'},
    )
    assert create_res.status_code == 201
    ocorr_id = create_res.json()['id']

    # Tramitar status para EM_ANDAMENTO
    patch_res = await async_client.patch(
        f'/api/v1/comunicacao/ocorrencias/{ocorr_id}/status',
        json={'status': 'EM_ANDAMENTO', 'mensagem': 'Encaminhado ao engenheiro predial para perícia técnica.'},
        headers={'Authorization': f'Bearer {sindico_token}'},
    )
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data['status'] == 'EM_ANDAMENTO'
    assert len(data['historico']) >= 1
    ultimo_historico = data['historico'][-1]
    assert ultimo_historico['tipo'] == 'MUDANCA_STATUS'
    assert 'engenheiro predial' in ultimo_historico['mensagem']


@pytest.mark.asyncio
async def test_consulta_ocorrencia_sigilosa_alheia_retorna_404(async_client: AsyncClient):
    morador_a_id = str(uuid.uuid4())
    morador_b_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())

    token_a = _make_token(morador_a_id, ['MORADOR'], condo_id)
    token_b = _make_token(morador_b_id, ['MORADOR'], condo_id)

    # Morador A abre ocorrência sigilosa
    create_res = await async_client.post(
        '/api/v1/comunicacao/ocorrencias',
        json={'titulo': 'Denúncia confidencial de uso indevido de vaga', 'descricao': 'Vaga ocupada sem autorização.', 'sigilosa': True},
        headers={'Authorization': f'Bearer {token_a}'},
    )
    assert create_res.status_code == 201
    ocorr_id = create_res.json()['id']

    # Morador B tenta acessar o detalhe direto da ocorrência sigilosa alheia -> 404
    detail_res = await async_client.get(
        f'/api/v1/comunicacao/ocorrencias/{ocorr_id}',
        headers={'Authorization': f'Bearer {token_b}'},
    )
    assert detail_res.status_code == 404


@pytest.mark.asyncio
async def test_fale_conosco_mensagem_sla_48h_201(async_client: AsyncClient):
    morador_id = str(uuid.uuid4())
    condo_id = str(uuid.uuid4())
    token = _make_token(morador_id, ['MORADOR'], condo_id)
    headers = {'Authorization': f'Bearer {token}'}

    payload = {
        'assunto': 'Dúvida sobre taxa extraordinária de reformas',
        'mensagem': 'Gostaria de entender o detalhamento das parcelas da reforma da fachada.',
    }
    res = await async_client.post('/api/v1/comunicacao/fale-conosco', json=payload, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data['id'] is not None
    assert data['assunto'] == payload['assunto']
    assert data['sla_horas'] == 48
    assert data['prazo_sla'] is not None
    assert data['status'] == 'NOVA_MENSAGEM'


@pytest.mark.asyncio
async def test_fale_conosco_listagem_isolada_por_unidade(async_client: AsyncClient):
    morador_a_id = str(uuid.uuid4())
    morador_b_id = str(uuid.uuid4())
    unidade_a_id = uuid.uuid4()
    unidade_b_id = uuid.uuid4()
    condo_id = str(uuid.uuid4())

    token_a = _make_token(morador_a_id, ['MORADOR'], condo_id)
    token_b = _make_token(morador_b_id, ['MORADOR'], condo_id)

    # Mensagem de A
    res_a = await async_client.post(
        '/api/v1/comunicacao/fale-conosco',
        json={'assunto': 'Solicitação de tag veicular extra', 'mensagem': 'Carro novo.', 'unidade_id': str(unidade_a_id)},
        headers={'Authorization': f'Bearer {token_a}'},
    )
    assert res_a.status_code == 201
    msg_a_id = res_a.json()['id']

    # Mensagem de B
    res_b = await async_client.post(
        '/api/v1/comunicacao/fale-conosco',
        json={'assunto': 'Dúvida sobre regras da academia', 'mensagem': 'Horários de sábado.', 'unidade_id': str(unidade_b_id)},
        headers={'Authorization': f'Bearer {token_b}'},
    )
    assert res_b.status_code == 201
    msg_b_id = res_b.json()['id']

    # Morador A consulta fale conosco -> só visualiza suas conversas
    list_a = await async_client.get(
        f'/api/v1/comunicacao/fale-conosco?unidade_id={unidade_a_id}',
        headers={'Authorization': f'Bearer {token_a}'},
    )
    assert list_a.status_code == 200
    ids_a = [m['id'] for m in list_a.json()]
    assert msg_a_id in ids_a
    assert msg_b_id not in ids_a
