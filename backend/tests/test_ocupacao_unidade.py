import uuid
from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient


@pytest.fixture
async def setup_cenario(async_client: AsyncClient):
    """Cria bloco, unidade e pessoas base para os testes de ocupação."""
    # 1. Criar Bloco e Unidade
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco Ocupacao'}
    )
    assert bloco_res.status_code == 201
    bloco_id = bloco_res.json()['id']

    unidade_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '101-A', 'andar': 1, 'bloco_id': bloco_id},
    )
    assert unidade_res.status_code == 201
    unidade_id = unidade_res.json()['id']

    # 2. Criar Pessoas
    pessoa_prop = (
        await async_client.post(
            '/api/v1/identidade/pessoas',
            json={'nome_completo': 'Carlos Proprietario', 'email': 'carlos@condo.com'},
        )
    ).json()

    pessoa_inq = (
        await async_client.post(
            '/api/v1/identidade/pessoas',
            json={'nome_completo': 'Mariana Inquilina', 'email': 'mariana@condo.com'},
        )
    ).json()

    pessoa_dep = (
        await async_client.post(
            '/api/v1/identidade/pessoas',
            json={'nome_completo': 'Pedrinho Dependente', 'email': 'pedrinho@condo.com'},
        )
    ).json()

    condominio_id = str(uuid.uuid4())

    return {
        'condominio_id': condominio_id,
        'unidade_id': unidade_id,
        'proprietario_id': pessoa_prop['id'],
        'inquilino_id': pessoa_inq['id'],
        'dependente_id': pessoa_dep['id'],
    }


@pytest.mark.asyncio
async def test_regra_1_proprietario_morador_bloqueado_com_inquilino_ativo(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 1: Se houver INQUILINO ATIVO, PROPRIETARIO não pode ter mora_no_local = TRUE."""
    c = setup_cenario

    # 1. Cadastra INQUILINO ativo na unidade
    inq_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'INQUILINO',
            'mora_no_local': True,
        },
    )
    assert inq_res.status_code == 201

    # 2. Tenta cadastrar PROPRIETARIO como morador local na mesma unidade -> DEVE FALHAR
    prop_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['proprietario_id'],
            'tipo_vinculo': 'PROPRIETARIO',
            'mora_no_local': True,
        },
    )
    assert prop_res.status_code == 400
    assert 'CONFLITO_POSSE_DIRETA' in prop_res.json()['detail']

    # 3. PROPRIETARIO com mora_no_local = False -> DEVE SER ACEITO
    prop_ok_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['proprietario_id'],
            'tipo_vinculo': 'PROPRIETARIO',
            'mora_no_local': False,
        },
    )
    assert prop_ok_res.status_code == 201
    assert prop_ok_res.json()['mora_no_local'] is False


@pytest.mark.asyncio
async def test_regra_1_ativacao_inquilino_desmarca_moradia_do_proprietario(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 1: Ao ativar INQUILINO, morador proprietário tem mora_no_local desmarcado automaticamente."""
    c = setup_cenario

    # 1. Proprietário inicialmente mora no local
    prop_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['proprietario_id'],
            'tipo_vinculo': 'PROPRIETARIO',
            'mora_no_local': True,
        },
    )
    assert prop_res.status_code == 201
    prop_id = prop_res.json()['id']
    assert prop_res.json()['mora_no_local'] is True

    # 2. Inquilino aluga a unidade
    inq_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'INQUILINO',
            'mora_no_local': True,
        },
    )
    assert inq_res.status_code == 201

    # 3. Consulta proprietário: mora_no_local deve ter virado False
    prop_check = await async_client.get(f'/api/v1/identidade/ocupacoes/{prop_id}')
    assert prop_check.status_code == 200
    assert prop_check.json()['mora_no_local'] is False


@pytest.mark.asyncio
async def test_regra_2_curto_prazo_temporario_e_hospede_exige_datas(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 2: TEMPORARIO ou HOSPEDE exigem data_inicio e data_fim obrigatoriamente."""
    c = setup_cenario

    # 1. TEMPORARIO sem data_fim -> DEVE FALHAR
    res_sem_fim = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'TEMPORARIO',
            'data_inicio': datetime.now(timezone.utc).isoformat(),
        },
    )
    assert res_sem_fim.status_code in (400, 422)

    # 2. HOSPEDE sem datas -> DEVE FALHAR
    res_sem_datas = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'HOSPEDE',
        },
    )
    assert res_sem_datas.status_code in (400, 422)

    # 3. TEMPORARIO com datas válidas -> SUCESSO
    inicio = datetime.now(timezone.utc)
    fim = inicio + timedelta(days=5)
    res_ok = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'TEMPORARIO',
            'data_inicio': inicio.isoformat(),
            'data_fim': fim.isoformat(),
        },
    )
    assert res_ok.status_code == 201
    assert res_ok.json()['tipo_vinculo'] == 'TEMPORARIO'
    assert res_ok.json()['fim_em'] is not None


@pytest.mark.asyncio
async def test_regra_3_retroatividade_data_fim_maior_que_inicio(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 3: data_fim deve ser estritamente maior que data_inicio."""
    c = setup_cenario
    agora = datetime.now(timezone.utc)

    # 1. data_fim anterior à data_inicio -> FALHA
    res_menor = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'TEMPORARIO',
            'inicio_em': agora.isoformat(),
            'fim_em': (agora - timedelta(hours=2)).isoformat(),
        },
    )
    assert res_menor.status_code in (400, 422)

    # 2. data_fim igual à data_inicio -> FALHA
    res_igual = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'TEMPORARIO',
            'inicio_em': agora.isoformat(),
            'fim_em': agora.isoformat(),
        },
    )
    assert res_igual.status_code in (400, 422)


@pytest.mark.asyncio
async def test_regra_4_bloqueio_automatico_rotina_expiracao(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 4: Rotina diária inativa ocupações com fim_em vencido."""
    c = setup_cenario
    passado_inicio = datetime.now(timezone.utc) - timedelta(days=10)
    passado_fim = datetime.now(timezone.utc) - timedelta(days=1)

    # 1. Cria ocupação temporária já vencida
    criacao = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'HOSPEDE',
            'inicio_em': passado_inicio.isoformat(),
            'fim_em': passado_fim.isoformat(),
        },
    )
    assert criacao.status_code == 201
    ocupacao_id = criacao.json()['id']
    assert criacao.json()['status'] == 'ATIVO'

    # 2. Dispara a rotina diária de expiração
    rotina_res = await async_client.post('/api/v1/identidade/ocupacoes/rotina-expiracao')
    assert rotina_res.status_code == 200
    dados_rotina = rotina_res.json()
    assert dados_rotina['ocupacoes_inativadas'] >= 1

    # 3. Confere que status mudou para INATIVO
    check_res = await async_client.get(f'/api/v1/identidade/ocupacoes/{ocupacao_id}')
    assert check_res.status_code == 200
    assert check_res.json()['status'] == 'INATIVO'


@pytest.mark.asyncio
async def test_regra_5_dependente_exige_responsavel_residente_ativo(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 5: DEPENDENTE só pode ser inserido se houver PROPRIETARIO morador ou INQUILINO ativo."""
    c = setup_cenario

    # 1. Unidade vazia: tenta inserir DEPENDENTE -> DEVE FALHAR
    dep_vazia = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['dependente_id'],
            'tipo_vinculo': 'DEPENDENTE',
        },
    )
    assert dep_vazia.status_code == 400
    assert 'DEPENDENTE_SEM_RESPONSAVEL_RESIDENTE' in dep_vazia.json()['detail']

    # 2. Unidade com proprietário que NÃO mora no local -> DEVE FALHAR
    await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['proprietario_id'],
            'tipo_vinculo': 'PROPRIETARIO',
            'mora_no_local': False,
        },
    )
    dep_prop_nao_mora = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['dependente_id'],
            'tipo_vinculo': 'DEPENDENTE',
        },
    )
    assert dep_prop_nao_mora.status_code == 400
    assert 'DEPENDENTE_SEM_RESPONSAVEL_RESIDENTE' in dep_prop_nao_mora.json()['detail']

    # 3. Inquilino ativo passa a residir na unidade -> DEPENDENTE DEVE SER ACEITO
    inq_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'INQUILINO',
            'mora_no_local': True,
        },
    )
    assert inq_res.status_code == 201
    inq_id = inq_res.json()['id']

    # 4. Agora insere dependente com responsavel_ocupacao_id do inquilino -> SUCESSO
    dep_ok = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['dependente_id'],
            'tipo_vinculo': 'DEPENDENTE',
            'responsavel_ocupacao_id': inq_id,
        },
    )
    assert dep_ok.status_code == 201
    assert dep_ok.json()['tipo_vinculo'] == 'DEPENDENTE'
    assert dep_ok.json()['responsavel_ocupacao_id'] == inq_id


@pytest.mark.asyncio
async def test_regra_5_inativacao_inquilino_cascadeia_dependentes(
    async_client: AsyncClient, setup_cenario: dict
):
    """Regra 5: Se inquilino for inativado, seus dependentes sofrem cascade para INATIVO."""
    c = setup_cenario

    # 1. Cadastra Inquilino
    inq_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['inquilino_id'],
            'tipo_vinculo': 'INQUILINO',
            'mora_no_local': True,
        },
    )
    inq_id = inq_res.json()['id']

    # 2. Cadastra Dependente atrelado a esse inquilino
    dep_res = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'condominio_id': c['condominio_id'],
            'unidade_id': c['unidade_id'],
            'pessoa_id': c['dependente_id'],
            'tipo_vinculo': 'DEPENDENTE',
            'responsavel_ocupacao_id': inq_id,
        },
    )
    dep_id = dep_res.json()['id']
    assert dep_res.json()['status'] == 'ATIVO'

    # 3. Inativa o inquilino com cascade_dependentes = True (padrão)
    inat_res = await async_client.post(
        f'/api/v1/identidade/ocupacoes/{inq_id}/inativar',
        json={'cascade_dependentes': True},
    )
    assert inat_res.status_code == 200
    assert inat_res.json()['dependentes_inativados'] == 1

    # 4. Confere que o dependente também foi cascadeado para INATIVO
    dep_check = await async_client.get(f'/api/v1/identidade/ocupacoes/{dep_id}')
    assert dep_check.status_code == 200
    assert dep_check.json()['status'] == 'INATIVO'
