import uuid
import pytest
from httpx import AsyncClient


@pytest.fixture
async def setup_bloco_unidade(async_client: AsyncClient):
    """Cria bloco e unidade para testes de onboarding, veículos e pets."""
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco Alpha Onboarding'}
    )
    assert bloco_res.status_code == 201
    bloco_id = bloco_res.json()['id']

    unidade_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '501-A', 'andar': 5, 'bloco_id': bloco_id},
    )
    assert unidade_res.status_code == 201
    unidade_id = unidade_res.json()['id']

    condominio_id = str(uuid.uuid4())

    return {
        'condominio_id': condominio_id,
        'bloco_id': bloco_id,
        'unidade_id': unidade_id,
    }


@pytest.mark.asyncio
async def test_solicitar_cadastro_morador_onboarding(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C16: Submissão de onboarding em POST /api/v1/identidade/onboarding/solicitar."""
    c = setup_bloco_unidade
    solicitacao_payload = {
        'unidade_id': c['unidade_id'],
        'nome_completo': 'Novo Residente Onboarding',
        'email': 'residente.onboarding@condourban.com.br',
        'celular': '11999998888',
        'tipo_vinculo': 'MORADOR',
        'condominio_id': c['condominio_id'],
    }
    res = await async_client.post(
        '/api/v1/identidade/onboarding/solicitar', json=solicitacao_payload
    )
    assert res.status_code == 201
    data = res.json()
    assert data['id'] is not None
    assert data['status'] == 'ENVIADA'
    assert data['unidade_id'] == c['unidade_id']


@pytest.mark.asyncio
async def test_listar_solicitacoes_onboarding(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C17: Listagem em GET /api/v1/identidade/onboarding/solicitacoes."""
    c = setup_bloco_unidade
    # Criar uma solicitação
    solicitacao_payload = {
        'unidade_id': c['unidade_id'],
        'nome_completo': 'Solicitante Fila',
        'email': 'solicitante.fila@condourban.com.br',
        'tipo_vinculo': 'INQUILINO',
        'condominio_id': c['condominio_id'],
    }
    await async_client.post(
        '/api/v1/identidade/onboarding/solicitar', json=solicitacao_payload
    )

    res = await async_client.get(
        f'/api/v1/identidade/onboarding/solicitacoes?condominio_id={c["condominio_id"]}'
    )
    assert res.status_code == 200
    lista = res.json()
    assert len(lista) >= 1
    assert any(s['unidade_id'] == c['unidade_id'] for s in lista)


@pytest.mark.asyncio
async def test_aprovar_solicitacao_gera_ocupacao(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C18: Aprovação transita status para APROVADA e cria ocupacao_unidade."""
    c = setup_bloco_unidade
    solicitacao_payload = {
        'unidade_id': c['unidade_id'],
        'nome_completo': 'Morador Aprovado',
        'email': 'aprovado@condourban.com.br',
        'tipo_vinculo': 'MORADOR',
        'condominio_id': c['condominio_id'],
    }
    sol_res = await async_client.post(
        '/api/v1/identidade/onboarding/solicitar', json=solicitacao_payload
    )
    sol_id = sol_res.json()['id']

    # Aprovar solicitação
    aprov_res = await async_client.post(
        f'/api/v1/identidade/onboarding/solicitacoes/{sol_id}/aprovar',
        json={'observacao': 'Documentos conferidos com sucesso.'},
    )
    assert aprov_res.status_code == 200
    aprov_data = aprov_res.json()
    assert aprov_data['status'] == 'APROVADA'
    assert aprov_data['ocupacao_id'] is not None

    # Consulta a ocupação criada
    ocup_id = aprov_data['ocupacao_id']
    ocup_res = await async_client.get(f'/api/v1/identidade/ocupacoes/{ocup_id}')
    assert ocup_res.status_code == 200
    assert ocup_res.json()['status'] == 'ATIVO'
    assert ocup_res.json()['mora_no_local'] is True


@pytest.mark.asyncio
async def test_rejeitar_solicitacao_validacao_motivo(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C19: Rejeição sem motivo_rejeicao retorna erro 400 ou 422; com motivo transita para REJEITADA."""
    c = setup_bloco_unidade
    sol_res = await async_client.post(
        '/api/v1/identidade/onboarding/solicitar',
        json={
            'unidade_id': c['unidade_id'],
            'nome_completo': 'Morador Rejeitado',
            'email': 'rejeitado@condourban.com.br',
            'tipo_vinculo': 'MORADOR',
            'condominio_id': c['condominio_id'],
        },
    )
    sol_id = sol_res.json()['id']

    # 1. Rejeitar sem motivo ou motivo em branco -> 400 ou 422
    rej_invalida = await async_client.post(
        f'/api/v1/identidade/onboarding/solicitacoes/{sol_id}/rejeitar',
        json={'motivo_rejeicao': '   '},
    )
    assert rej_invalida.status_code in (400, 422)

    # 2. Rejeitar com motivo válido -> 200
    rej_valida = await async_client.post(
        f'/api/v1/identidade/onboarding/solicitacoes/{sol_id}/rejeitar',
        json={'motivo_rejeicao': 'Comprovante de residência ilegível.'},
    )
    assert rej_valida.status_code == 200
    assert rej_valida.json()['status'] == 'REJEITADA'
    assert rej_valida.json()['motivo_rejeicao'] == 'Comprovante de residência ilegível.'


@pytest.mark.asyncio
async def test_cadastrar_e_listar_veiculo_placa_maiuscula(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C20: Cadastro grava placa em caixa alta com status 201 e GET lista veículos."""
    c = setup_bloco_unidade
    veiculo_payload = {
        'condominio_id': c['condominio_id'],
        'unidade_id': c['unidade_id'],
        'placa': 'abc-1d23',  # minúsculo com hífen
        'tipo': 'CARRO',
        'marca': 'Toyota',
        'modelo': 'Corolla',
        'cor': 'Prata',
    }
    res = await async_client.post(
        '/api/v1/identidade/veiculos-pets/veiculos', json=veiculo_payload
    )
    assert res.status_code == 201
    data = res.json()
    assert data['placa'] == 'ABC1D23'
    assert data['tipo'] == 'CARRO'

    # Listagem
    list_res = await async_client.get(
        f'/api/v1/identidade/veiculos-pets/veiculos?condominio_id={c["condominio_id"]}'
    )
    assert list_res.status_code == 200
    veiculos = list_res.json()
    assert len(veiculos) >= 1
    assert veiculos[0]['placa'] == 'ABC1D23'


@pytest.mark.asyncio
async def test_duplicidade_placa_no_condominio_rejeitada(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C21: Tentativa de cadastrar a mesma placa veicular no mesmo condomínio retorna status 400."""
    c = setup_bloco_unidade
    # 1. Cadastra na unidade 501
    veiculo_1 = {
        'condominio_id': c['condominio_id'],
        'unidade_id': c['unidade_id'],
        'placa': 'XYZ9988',
        'tipo': 'CARRO',
        'marca': 'Honda',
        'modelo': 'Civic',
    }
    res1 = await async_client.post(
        '/api/v1/identidade/veiculos-pets/veiculos', json=veiculo_1
    )
    assert res1.status_code == 201

    # 2. Cria outra unidade no mesmo condomínio
    unidade_2_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '502-A', 'andar': 5, 'bloco_id': c['bloco_id']},
    )
    unidade_2_id = unidade_2_res.json()['id']

    # 3. Tenta cadastrar mesma placa na nova unidade -> 400
    veiculo_2 = {
        'condominio_id': c['condominio_id'],
        'unidade_id': unidade_2_id,
        'placa': 'xyz-9988',  # mesma placa com formato diferente
        'tipo': 'CARRO',
    }
    res2 = await async_client.post(
        '/api/v1/identidade/veiculos-pets/veiculos', json=veiculo_2
    )
    assert res2.status_code == 400
    assert 'PLACA_DUPLICADA' in res2.json()['detail']


@pytest.mark.asyncio
async def test_cadastrar_e_listar_pets(
    async_client: AsyncClient, setup_bloco_unidade: dict
):
    """C22: Cadastro de pet com status 201 e listagem com status 200."""
    c = setup_bloco_unidade
    pet_payload = {
        'condominio_id': c['condominio_id'],
        'unidade_id': c['unidade_id'],
        'nome': 'Rex',
        'especie': 'CANINO',
        'raca': 'Golden Retriever',
        'porte': 'GRANDE',
        'cor': 'Dourado',
        'vacinado': True,
    }
    res = await async_client.post(
        '/api/v1/identidade/veiculos-pets/pets', json=pet_payload
    )
    assert res.status_code == 201
    pet_data = res.json()
    assert pet_data['id'] is not None
    assert pet_data['nome'] == 'Rex'
    assert pet_data['porte'] == 'GRANDE'
    assert pet_data['vacinado'] is True

    # Listagem
    list_res = await async_client.get(
        f'/api/v1/identidade/veiculos-pets/pets?condominio_id={c["condominio_id"]}'
    )
    assert list_res.status_code == 200
    pets = list_res.json()
    assert len(pets) >= 1
    assert pets[0]['nome'] == 'Rex'
