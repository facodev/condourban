import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'


@pytest.mark.asyncio
async def test_blocos_crud(async_client: AsyncClient):
    # Criar bloco (C1)
    create_payload = {
        'nome': 'Bloco A',
        'descricao': 'Bloco residencial central',
    }
    post_res = await async_client.post(
        '/api/v1/condominio/blocos', json=create_payload
    )
    assert post_res.status_code == 201
    bloco = post_res.json()
    assert bloco['id'] is not None
    assert bloco['nome'] == 'Bloco A'
    assert bloco['descricao'] == 'Bloco residencial central'

    # Listar blocos (C2)
    get_res = await async_client.get('/api/v1/condominio/blocos')
    assert get_res.status_code == 200
    blocos = get_res.json()
    assert len(blocos) >= 1
    assert any(b['nome'] == 'Bloco A' for b in blocos)


@pytest.mark.asyncio
async def test_unidades_crud(async_client: AsyncClient):
    # Criar bloco pai
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco B'}
    )
    bloco_id = bloco_res.json()['id']

    # Criar unidade (C3)
    unit_payload = {
        'identificacao': '101',
        'andar': '1',
        'bloco_id': bloco_id,
    }
    post_res = await async_client.post(
        '/api/v1/condominio/unidades', json=unit_payload
    )
    assert post_res.status_code == 201
    unit = post_res.json()
    assert unit['identificacao'] == '101'
    assert unit['bloco_id'] == bloco_id

    # Listar unidades (C6)
    get_res = await async_client.get('/api/v1/condominio/unidades')
    assert get_res.status_code == 200
    unidades = get_res.json()
    assert len(unidades) >= 1
    assert any(u['identificacao'] == '101' for u in unidades)


@pytest.mark.asyncio
async def test_unidade_duplicada_no_bloco_retorna_400(async_client: AsyncClient):
    """C4: Unidade com mesma identificação no mesmo bloco retorna 400 UNIDADE_DUPLICADA."""
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco Bronze'}
    )
    bloco_id = bloco_res.json()['id']

    unit_payload = {
        'identificacao': '301',
        'andar': 3,
        'bloco_id': bloco_id,
    }
    res1 = await async_client.post('/api/v1/condominio/unidades', json=unit_payload)
    assert res1.status_code == 201

    res2 = await async_client.post('/api/v1/condominio/unidades', json=unit_payload)
    assert res2.status_code == 400
    assert res2.json()['detail'] == 'UNIDADE_DUPLICADA'


@pytest.mark.asyncio
async def test_importar_unidades_csv(async_client: AsyncClient):
    """C5: Importação em lote via CSV em POST /api/v1/condominio/unidades/importar."""
    csv_content = 'identificacao,andar,bloco\n401,4,Bloco CSV\n402,4,Bloco CSV\n'
    condominio_id = str(uuid.uuid4())
    res = await async_client.post(
        f'/api/v1/condominio/unidades/importar?condominio_id={condominio_id}',
        json={'arquivo_csv': csv_content},
    )
    assert res.status_code == 200
    data = res.json()
    assert data['unidades_criadas'] == 2


@pytest.mark.asyncio
async def test_cadastrar_e_listar_vagas_garagem(async_client: AsyncClient):
    """C7 e C9: Cadastro de vaga de garagem com status 201 e listagem com status 200."""
    condominio_id = str(uuid.uuid4())
    vaga_payload = {
        'condominio_id': condominio_id,
        'identificacao': 'V-01',
        'tipo': 'CARRO',
        'coberta': True,
    }
    res_post = await async_client.post(
        '/api/v1/condominio/vagas', json=vaga_payload
    )
    assert res_post.status_code == 201
    data = res_post.json()
    assert data['id'] is not None
    assert data['identificacao'] == 'V-01'
    assert data['coberta'] is True

    # Listagem (C9)
    res_get = await async_client.get(
        f'/api/v1/condominio/vagas?condominio_id={condominio_id}'
    )
    assert res_get.status_code == 200
    vagas = res_get.json()
    assert len(vagas) == 1
    assert vagas[0]['identificacao'] == 'V-01'


@pytest.mark.asyncio
async def test_vaga_duplicada_no_condominio_retorna_400(async_client: AsyncClient):
    """C8: Vaga com mesma identificação no mesmo condomínio retorna 400 VAGA_DUPLICADA."""
    condominio_id = str(uuid.uuid4())
    vaga_payload = {
        'condominio_id': condominio_id,
        'identificacao': 'V-DUP',
        'tipo': 'CARRO',
    }
    res1 = await async_client.post(
        '/api/v1/condominio/vagas', json=vaga_payload
    )
    assert res1.status_code == 201

    res2 = await async_client.post(
        '/api/v1/condominio/vagas', json=vaga_payload
    )
    assert res2.status_code == 400
    assert res2.json()['detail'] == 'VAGA_DUPLICADA'


@pytest.mark.asyncio
async def test_atualizar_vinculo_vaga_garagem(async_client: AsyncClient):
    """C10: PATCH /api/v1/condominio/vagas/{id} vincula unidade habitacional."""
    condominio_id = str(uuid.uuid4())
    vaga_res = await async_client.post(
        '/api/v1/condominio/vagas',
        json={'condominio_id': condominio_id, 'identificacao': 'V-100', 'coberta': False},
    )
    vaga_id = vaga_res.json()['id']

    # Criar unidade
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco Vagas', 'condominio_id': condominio_id}
    )
    bloco_id = bloco_res.json()['id']
    unidade_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '901', 'andar': 9, 'bloco_id': bloco_id, 'condominio_id': condominio_id},
    )
    unidade_id = unidade_res.json()['id']

    # Atualizar vaga associando à unidade
    patch_res = await async_client.patch(
        f'/api/v1/condominio/vagas/{vaga_id}',
        json={'unidade_id': unidade_id, 'coberta': True},
    )
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data['unidade_id'] == unidade_id
    assert data['coberta'] is True


@pytest.mark.asyncio
async def test_areas_comuns_crud(async_client: AsyncClient):
    """C11 e C12: Cadastro em POST e listagem em GET /api/v1/condominio/areas-comuns."""
    area_payload = {
        'nome': 'Salão Gourmet',
        'capacidade': 60,
        'requer_aprovacao': True,
        'horario_abertura': '09:00',
        'horario_fechamento': '23:00',
    }
    post_res = await async_client.post(
        '/api/v1/condominio/areas-comuns', json=area_payload
    )
    assert post_res.status_code == 201
    area = post_res.json()
    assert area['nome'] == 'Salão Gourmet'
    assert area['capacidade'] == 60
    assert area['requer_aprovacao'] is True

    get_res = await async_client.get('/api/v1/condominio/areas-comuns')
    assert get_res.status_code == 200
    areas = get_res.json()
    assert len(areas) >= 1
    assert any(a['nome'] == 'Salão Gourmet' for a in areas)


@pytest.mark.asyncio
async def test_areas_comuns_detalhe_e_interdicao(async_client: AsyncClient):
    """C13 e C14: GET /{id} e PATCH /{id} para interdição de espaço comum."""
    post_res = await async_client.post(
        '/api/v1/condominio/areas-comuns',
        json={'nome': 'Piscina Olímpica', 'capacidade': 120, 'ativo': True},
    )
    area_id = post_res.json()['id']

    # Consulta por ID (C13)
    get_res = await async_client.get(f'/api/v1/condominio/areas-comuns/{area_id}')
    assert get_res.status_code == 200
    assert get_res.json()['nome'] == 'Piscina Olímpica'

    # Interdição / alteração de status (C14)
    patch_res = await async_client.patch(
        f'/api/v1/condominio/areas-comuns/{area_id}',
        json={'ativo': False},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()['ativo'] is False


@pytest.mark.asyncio
async def test_condominio_info_crud(async_client: AsyncClient):
    """C15 e C16: GET /info e PUT /info para dados cadastrais e endereço."""
    # Consulta cadastral (C15)
    info_res = await async_client.get('/api/v1/condominio/info')
    assert info_res.status_code == 200
    data = info_res.json()
    assert 'nome' in data

    # Atualização cadastral (C16)
    update_payload = {
        'nome': 'Condomínio Residencial Jardins',
        'razao_social': 'Condomínio Residencial Jardins SPE Ltda',
        'cidade': 'Campinas',
        'uf': 'SP',
    }
    put_res = await async_client.put(
        '/api/v1/condominio/info', json=update_payload
    )
    assert put_res.status_code == 200
    updated = put_res.json()
    assert updated['nome'] == 'Condomínio Residencial Jardins'
    assert updated['cidade'] == 'Campinas'


@pytest.mark.asyncio
async def test_condominio_configuracoes_branding_regras(async_client: AsyncClient):
    """C17 e C18: GET /configuracoes e PATCH /configuracoes para branding e convivência."""
    # Consulta configurações (C17)
    get_res = await async_client.get('/api/v1/condominio/configuracoes')
    assert get_res.status_code == 200
    configs = get_res.json()
    assert isinstance(configs, dict)

    # Atualização parcial (C18)
    patch_payload = {
        'branding': {
            'nome_fantasia': 'Residencial Jardins',
            'cor_primaria': '#0F766E',
        },
        'regras_operacionais': {
            'horario_silencio_inicio': '22:30',
            'horario_silencio_fim': '07:30',
        },
    }
    patch_res = await async_client.patch(
        '/api/v1/condominio/configuracoes', json=patch_payload
    )
    assert patch_res.status_code == 200
    saved = patch_res.json()
    assert saved['branding']['cor_primaria'] == '#0F766E'
    assert saved['regras_operacionais']['horario_silencio_inicio'] == '22:30'


@pytest.mark.asyncio
async def test_condominio_persistencia_razao_social(async_client: AsyncClient):
    """Verifica persistência de razão social mesmo enviada em camelCase (razaoSocial)."""
    novo_c = await async_client.post(
        '/api/v1/condominio/novo',
        json={'nome': 'Condomínio Teste Persistência', 'razao_social': 'Razao Inicial Ltda'},
    )
    assert novo_c.status_code == 201
    c_id = novo_c.json()['id']

    # Atualiza enviando razaoSocial (camelCase do Angular)
    update_res = await async_client.put(
        f'/api/v1/condominio/info?condominio_id={c_id}',
        json={'razaoSocial': 'Razao Social Persistida e Atualizada S/A', 'nome': 'Condomínio Teste Persistência'},
    )
    assert update_res.status_code == 200
    res_data = update_res.json()
    assert res_data['razao_social'] == 'Razao Social Persistida e Atualizada S/A'
    assert res_data['razaoSocial'] == 'Razao Social Persistida e Atualizada S/A'

    # Consulta novamente
    get_res = await async_client.get(f'/api/v1/condominio/info?condominio_id={c_id}')
    assert get_res.status_code == 200
    assert get_res.json()['razao_social'] == 'Razao Social Persistida e Atualizada S/A'


@pytest.mark.asyncio
async def test_isolamento_multi_condominio(async_client: AsyncClient):
    """Garante que blocos e unidades de um condomínio não vazam para outro."""
    # Criar Condomínio Alfa
    res_a = await async_client.post('/api/v1/condominio/novo', json={'nome': 'Condomínio Alfa'})
    assert res_a.status_code == 201
    condo_a_id = res_a.json()['id']

    # Criar Condomínio Beta
    res_b = await async_client.post('/api/v1/condominio/novo', json={'nome': 'Condomínio Beta'})
    assert res_b.status_code == 201
    condo_b_id = res_b.json()['id']

    # Criar bloco em Alfa via header X-Condominio-Id
    res_bloco_a = await async_client.post(
        '/api/v1/condominio/blocos',
        json={'nome': 'Torre Alfa 1'},
        headers={'X-Condominio-Id': condo_a_id},
    )
    assert res_bloco_a.status_code == 201

    # Criar bloco em Beta via header X-Condominio-Id
    res_bloco_b = await async_client.post(
        '/api/v1/condominio/blocos',
        json={'nome': 'Torre Beta 1'},
        headers={'X-Condominio-Id': condo_b_id},
    )
    assert res_bloco_b.status_code == 201

    # Listar blocos de Alfa
    list_a = await async_client.get(
        '/api/v1/condominio/blocos',
        headers={'X-Condominio-Id': condo_a_id},
    )
    assert list_a.status_code == 200
    nomes_a = [b['nome'] for b in list_a.json()]
    assert 'Torre Alfa 1' in nomes_a
    assert 'Torre Beta 1' not in nomes_a

    # Listar blocos de Beta
    list_b = await async_client.get(
        '/api/v1/condominio/blocos',
        headers={'X-Condominio-Id': condo_b_id},
    )
    assert list_b.status_code == 200
    nomes_b = [b['nome'] for b in list_b.json()]
    assert 'Torre Beta 1' in nomes_b
    assert 'Torre Alfa 1' not in nomes_b


@pytest.mark.asyncio
async def test_areas_comuns_edicao_e_regras_dias(async_client: AsyncClient):
    """Cria e edita área comum com suporte a regras de horários e valores por dia da semana."""
    # Criar espaço
    regras = {
        'segunda': {'aberto': False, 'horario_abertura': '08:00', 'horario_fechamento': '22:00', 'valor': 0},
        'sabado': {'aberto': True, 'horario_abertura': '08:00', 'horario_fechamento': '23:59', 'valor': 350.0},
        'domingo': {'aberto': True, 'horario_abertura': '08:00', 'horario_fechamento': '22:00', 'valor': 300.0},
    }
    c_res = await async_client.post(
        '/api/v1/condominio/areas-comuns',
        json={
            'nome': 'Espaço Gourmet VIP',
            'capacidade': 40,
            'taxa_reserva': 150.0,
            'horario_abertura': '09:00',
            'horario_fechamento': '22:00',
            'regras_dias': regras,
        },
    )
    assert c_res.status_code == 201
    area = c_res.json()
    area_id = area['id']
    assert area['nome'] == 'Espaço Gourmet VIP'
    assert area['regras_dias']['sabado']['valor'] == 350.0

    # Editar espaço comum (PATCH)
    edit_payload = {
        'nome': 'Espaço Gourmet VIP Master',
        'capacidade': 50,
        'taxa_reserva': 180.0,
        'regras_dias': {
            **regras,
            'sexta': {'aberto': True, 'horario_abertura': '09:00', 'horario_fechamento': '23:00', 'valor': 250.0},
        },
    }
    patch_res = await async_client.patch(
        f'/api/v1/condominio/areas-comuns/{area_id}',
        json=edit_payload,
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated['nome'] == 'Espaço Gourmet VIP Master'
    assert updated['capacidade'] == 50
    assert 'sexta' in updated['regras_dias']
    assert updated['regras_dias']['sexta']['valor'] == 250.0
