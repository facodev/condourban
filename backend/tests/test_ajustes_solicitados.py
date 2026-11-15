import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_area_comum_com_descricao(async_client: AsyncClient):
    """Testa cadastro e atualização de área comum com texto informativo para moradores."""
    # Criar área comum com descrição / orientações para moradores
    payload = {
        'nome': 'Salão Gourmet Teste',
        'capacidade': 30,
        'taxa_reserva': 150.00,
        'descricao': 'Uso liberado até às 23h. É proibido som automotivo. Retirar lixo após o evento.',
    }
    res_area = await async_client.post(
        '/api/v1/condominio/areas-comuns',
        json=payload,
    )
    assert res_area.status_code == 201
    area_data = res_area.json()
    assert area_data['descricao'] == payload['descricao']

    # Atualizar descrição
    res_update = await async_client.put(
        f"/api/v1/condominio/areas-comuns/{area_data['id']}",
        json={'descricao': 'Novo texto de regras e informações.'},
    )
    assert res_update.status_code == 200
    assert res_update.json()['descricao'] == 'Novo texto de regras e informações.'


@pytest.mark.asyncio
async def test_vaga_editar_identificacao(async_client: AsyncClient):
    """Testa que é permitido editar a identificação da vaga de garagem."""
    condominio_id = str(uuid.uuid4())

    # Cria vaga 1
    res_vaga1 = await async_client.post(
        '/api/v1/condominio/vagas',
        json={'identificacao': 'V-101', 'tipo': 'CARRO', 'coberta': True, 'condominio_id': condominio_id},
    )
    assert res_vaga1.status_code == 201
    vaga1_id = res_vaga1.json()['id']

    # Cria vaga 2
    res_vaga2 = await async_client.post(
        '/api/v1/condominio/vagas',
        json={'identificacao': 'V-102', 'tipo': 'CARRO', 'coberta': False, 'condominio_id': condominio_id},
    )
    assert res_vaga2.status_code == 201
    vaga2_id = res_vaga2.json()['id']

    # Edita identificação da vaga 1
    res_patch = await async_client.patch(
        f'/api/v1/condominio/vagas/{vaga1_id}',
        json={'identificacao': 'V-101-NOVA'},
    )
    assert res_patch.status_code == 200
    assert res_patch.json()['identificacao'] == 'V-101-NOVA'

    # Tenta renomear vaga 2 para a mesma da vaga 1 (deve falhar por duplicidade)
    res_dup = await async_client.patch(
        f'/api/v1/condominio/vagas/{vaga2_id}',
        json={'identificacao': 'V-101-NOVA'},
    )
    assert res_dup.status_code == 400
    assert 'VAGA_DUPLICADA' in res_dup.json()['detail']


@pytest.mark.asyncio
async def test_pessoa_validacao_cpf_e_telefones(async_client: AsyncClient):
    """Testa validação de CPF e suporte a múltiplos telefones tipados e WhatsApp."""
    # 1. CPF Inválido
    res_cpf_inv = await async_client.post(
        '/api/v1/identidade/pessoas',
        json={'nome': 'Teste CPF', 'email': 'cpf.invalido@teste.com', 'cpf': '123.456.789-00'},
    )
    assert res_cpf_inv.status_code == 422

    # 2. Email Inválido
    res_email_inv = await async_client.post(
        '/api/v1/identidade/pessoas',
        json={'nome': 'Teste Email', 'email': 'invalido-sem-arroba'},
    )
    assert res_email_inv.status_code == 422

    # 3. Pessoa válida com CPF e múltiplos telefones (celular + residencial + comercial)
    # CPF válido de teste: 52998224725
    payload_valido = {
        'nome': 'Morador Completo Silva',
        'email': 'morador.silva@exemplo.com',
        'cpf': '52998224725',
        'telefones': [
            {'numero': '11987654321', 'tipo': 'celular', 'principal': True, 'whatsapp': True},
            {'numero': '1134567890', 'tipo': 'residencial', 'principal': False, 'whatsapp': False},
            {'numero': '1123456789', 'tipo': 'comercial', 'principal': False, 'whatsapp': True},
        ],
    }
    res_pessoa = await async_client.post(
        '/api/v1/identidade/pessoas',
        json=payload_valido,
    )
    assert res_pessoa.status_code == 201
    dados = res_pessoa.json()
    assert len(dados['telefones']) == 3
    assert dados['celular'] == '11987654321'
    p_id = dados['id']

    # 4. Tentar duplicar tipo de telefone (ex: dois celulares)
    res_dup_tipo = await async_client.patch(
        f'/api/v1/identidade/pessoas/{p_id}',
        json={
            'telefones': [
                {'numero': '11987654321', 'tipo': 'celular', 'principal': True, 'whatsapp': True},
                {'numero': '11999998888', 'tipo': 'celular', 'principal': False, 'whatsapp': False},
            ]
        },
    )
    assert res_dup_tipo.status_code == 422


@pytest.mark.asyncio
async def test_ocupacao_editar_unidade(async_client: AsyncClient):
    """Testa que é permitido alterar a unidade de um vínculo habitacional na edição."""
    # Cria bloco
    res_bloco = await async_client.post(
        '/api/v1/condominio/blocos',
        json={'nome': 'Bloco A'},
    )
    bloco_id = res_bloco.json()['id']

    # Cria unidade 1
    res_u1 = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '101', 'bloco_id': bloco_id},
    )
    u1_id = res_u1.json()['id']

    # Cria unidade 2
    res_u2 = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '102', 'bloco_id': bloco_id},
    )
    u2_id = res_u2.json()['id']

    # Cria pessoa
    res_p = await async_client.post(
        '/api/v1/identidade/pessoas',
        json={'nome': 'Proprietário Unidade', 'email': 'prop.unid@teste.com'},
    )
    p_id = res_p.json()['id']

    # Cria ocupação vinculada a u1
    res_oc = await async_client.post(
        '/api/v1/identidade/ocupacoes',
        json={
            'unidade_id': u1_id,
            'pessoa_id': p_id,
            'tipo_vinculo': 'PROPRIETARIO',
            'mora_no_local': True,
        },
    )
    assert res_oc.status_code == 201
    oc_id = res_oc.json()['id']
    assert res_oc.json()['unidade_id'] == u1_id

    # Edita vínculo mudando para u2
    res_patch = await async_client.patch(
        f'/api/v1/identidade/ocupacoes/{oc_id}',
        json={'unidade_id': u2_id},
    )
    assert res_patch.status_code == 200
    assert res_patch.json()['unidade_id'] == u2_id
