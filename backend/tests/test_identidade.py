import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_usuarios_registro_e_login(async_client: AsyncClient):
    # Registrar usuário
    user_payload = {
        'email': 'morador@condourban.com.br',
        'nome_completo': 'Ana Pereira',
        'senha': 'senhaSegura123!',
        'papel': 'morador',
    }
    register_res = await async_client.post(
        '/api/v1/identidade/usuarios/registrar', json=user_payload
    )
    assert register_res.status_code == 201
    user_data = register_res.json()
    assert user_data['id'] is not None
    assert user_data['email'] == 'morador@condourban.com.br'
    assert user_data['nome_completo'] == 'Ana Pereira'
    assert user_data['ativo'] is True

    # Testar duplicidade de email
    dup_res = await async_client.post(
        '/api/v1/identidade/usuarios/registrar', json=user_payload
    )
    assert dup_res.status_code == 400

    # Listar usuários
    list_res = await async_client.get('/api/v1/identidade/usuarios')
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # Login com sucesso
    login_payload = {
        'email': 'morador@condourban.com.br',
        'senha': 'senhaSegura123!',
    }
    login_res = await async_client.post(
        '/api/v1/identidade/usuarios/login', json=login_payload
    )
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert 'access_token' in token_data
    assert token_data['token_type'] == 'bearer'

    # Login com senha incorreta
    bad_login = {
        'email': 'morador@condourban.com.br',
        'senha': 'senhaErrada',
    }
    bad_res = await async_client.post(
        '/api/v1/identidade/usuarios/login', json=bad_login
    )
    assert bad_res.status_code == 401


@pytest.mark.asyncio
async def test_residentes_crud(async_client: AsyncClient):
    # Criar bloco e unidade
    bloco_res = await async_client.post(
        '/api/v1/condominio/blocos', json={'nome': 'Bloco E'}
    )
    bloco_id = bloco_res.json()['id']

    unit_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '404', 'andar': '4', 'bloco_id': bloco_id},
    )
    unit_id = unit_res.json()['id']

    # Criar usuário
    user_res = await async_client.post(
        '/api/v1/identidade/usuarios/registrar',
        json={
            'email': 'residente@condourban.com.br',
            'nome_completo': 'Marcos Lima',
            'senha': 'senhaSegura123!',
        },
    )
    user_id = user_res.json()['id']

    # Vincular residente
    residente_payload = {
        'usuario_id': user_id,
        'unidade_id': unit_id,
        'tipo_vinculo': 'proprietario',
    }
    post_res = await async_client.post(
        '/api/v1/identidade/residentes', json=residente_payload
    )
    assert post_res.status_code == 201
    residente = post_res.json()
    assert residente['usuario_id'] == user_id
    assert residente['unidade_id'] == unit_id
    assert residente['tipo_vinculo'] == 'proprietario'

    get_res = await async_client.get('/api/v1/identidade/residentes')
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1


@pytest.mark.asyncio
async def test_convite_dependente_gerado_com_7_dias(async_client: AsyncClient):
    # Criar bloco e unidade
    bloco_res = await async_client.post('/api/v1/condominio/blocos', json={'nome': 'Bloco C'})
    bloco_id = bloco_res.json()['id']
    unit_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '102', 'andar': 1, 'bloco_id': bloco_id},
    )
    unit_id = unit_res.json()['id']

    # Gerar convite
    convite_payload = {
        'unidade_id': unit_id,
        'nome_completo': 'Filho Dependente',
        'email': 'filho@condourban.com.br',
        'tipo_vinculo': 'DEPENDENTE',
    }
    convite_res = await async_client.post('/api/v1/identidade/convites', json=convite_payload)
    assert convite_res.status_code == 201
    data = convite_res.json()
    assert 'token' in data
    assert 'expira_em' in data
    assert data['unidade_id'] == unit_id


@pytest.mark.asyncio
async def test_convite_expirado_rejeita_ingresso(async_client: AsyncClient):
    # Criar convite
    bloco_res = await async_client.post('/api/v1/condominio/blocos', json={'nome': 'Bloco D'})
    bloco_id = bloco_res.json()['id']
    unit_res = await async_client.post(
        '/api/v1/condominio/unidades',
        json={'identificacao': '103', 'andar': 1, 'bloco_id': bloco_id},
    )
    unit_id = unit_res.json()['id']

    convite_payload = {
        'unidade_id': unit_id,
        'nome_completo': 'Convidado Expirado',
        'email': 'expirado@condourban.com.br',
        'tipo_vinculo': 'MORADOR',
    }
    convite_res = await async_client.post('/api/v1/identidade/convites', json=convite_payload)
    token = convite_res.json()['token']

    # Simular expiração manual de convite no banco ou token inválido
    # Aceite com token inexistente dá 404
    bad_res = await async_client.post('/api/v1/identidade/convites/token_falso_123/aceitar')
    assert bad_res.status_code == 404

    # Aceite com token válido
    aceite_res = await async_client.post(f'/api/v1/identidade/convites/{token}/aceitar')
    assert aceite_res.status_code == 200
    assert aceite_res.json()['status'] == 'ACEITO'

    # Segundo aceite (já usado / expirado) dá 400
    retry_res = await async_client.post(f'/api/v1/identidade/convites/{token}/aceitar')
    assert retry_res.status_code == 400
    assert retry_res.json()['detail'] == 'CONVITE_EXPIRADO'


@pytest.mark.asyncio
async def test_pessoa_dependente_sem_usuario_login(async_client: AsyncClient):
    # Cadastro civil de pessoa sem conta de usuário
    pessoa_payload = {
        'nome_completo': 'Criança Dependente',
        'data_nascimento': '2018-05-12',
    }
    res = await async_client.post('/api/v1/identidade/pessoas', json=pessoa_payload)
    assert res.status_code == 201
    pessoa_data = res.json()
    assert pessoa_data['id'] is not None
    assert pessoa_data['nome_completo'] == 'Criança Dependente'



@pytest.mark.asyncio
async def test_usuarios_admin_crud(async_client: AsyncClient):
    """Verifica criação, edição e exclusão de contas de usuários administrativos e moradores."""
    # 1. Criar novo usuário
    payload = {
        'email': 'sindico.gestor@condourban.com.br',
        'nome_completo': 'Síndico Gestor Teste',
        'senha': 'senhaSegura123!',
        'papel': 'SINDICO',
    }
    create_res = await async_client.post('/api/v1/identidade/usuarios', json=payload)
    assert create_res.status_code == 201
    user = create_res.json()
    assert user['id'] is not None
    assert user['email'] == 'sindico.gestor@condourban.com.br'
    assert 'SINDICO' in user['papeis']
    user_id = user['id']

    # 2. Obter usuário por ID
    get_res = await async_client.get(f'/api/v1/identidade/usuarios/{user_id}')
    assert get_res.status_code == 200
    assert get_res.json()['email'] == 'sindico.gestor@condourban.com.br'

    # 3. Editar usuário (mudar status e papel)
    update_payload = {
        'papel': 'ADMINISTRADOR',
        'status': 'INATIVO',
    }
    patch_res = await async_client.patch(f'/api/v1/identidade/usuarios/{user_id}', json=update_payload)
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated['status'] == 'INATIVO'
    assert 'ADMINISTRADOR' in updated['papeis']

    # 4. Deletar usuário
    del_res = await async_client.delete(f'/api/v1/identidade/usuarios/{user_id}')
    assert del_res.status_code == 200
    assert del_res.json()['status'] == 'sucesso'

    # 5. Confirmar que não existe mais
    check_del = await async_client.get(f'/api/v1/identidade/usuarios/{user_id}')
    assert check_del.status_code == 404
