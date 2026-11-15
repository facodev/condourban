import uuid
from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import ActiveCondominioDep, CurrentUserDep, SessionDep
from app.core.rbac import (
    assert_pessoa_no_escopo,
    ids_pessoas_visiveis,
    negar_gestao_cadastro,
    resolver_escopo_cadastro,
)
from .schemas import (
    PessoaCreate,
    PessoaResponse,
    PessoaUpdate,
)
from .service import PessoaService

router = APIRouter(tags=['Identidade - Pessoas'])


@router.get('/pessoas/me', response_model=PessoaResponse)
async def get_my_profile(
    db: SessionDep, current_user: CurrentUserDep
) -> PessoaResponse:
    service = PessoaService(db)
    return await service.get_me(current_user['user_id'])


@router.get('/pessoas', response_model=list[PessoaResponse])
@router.get('/residentes', response_model=list[PessoaResponse], include_in_schema=False)
async def list_persons(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> list[PessoaResponse]:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = PessoaService(db)
    if c_id:
        ids = await ids_pessoas_visiveis(db, escopo, c_id)
        return await service.list_pessoas(pessoa_ids=ids, condominio_id=c_id)
    return await service.list_pessoas(pessoa_ids=None, condominio_id=None)


@router.get('/pessoas/{id}', response_model=PessoaResponse)
async def get_person(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> PessoaResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    if c_id:
        await assert_pessoa_no_escopo(db, escopo, id, c_id)
    service = PessoaService(db)
    return await service.get_pessoa(id)


@router.post(
    '/pessoas', response_model=PessoaResponse, status_code=status.HTTP_201_CREATED
)
@router.post(
    '/residentes',
    response_model=PessoaResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_person(
    dto: PessoaCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> PessoaResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = PessoaService(db)
    return await service.create_pessoa(dto, condominio_id=c_id)


@router.patch('/pessoas/{id}', response_model=PessoaResponse)
@router.put('/pessoas/{id}', response_model=PessoaResponse, include_in_schema=False)
async def update_person(
    id: uuid.UUID,
    dto: PessoaUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> PessoaResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    if c_id:
        await assert_pessoa_no_escopo(db, escopo, id, c_id)

    # Síndico/admin: edição civil completa
    # Morador (e portaria sobre si): só campos de contato
    # Portaria NÃO edita cadastro de terceiros
    if escopo.get('pode_editar'):
        somente_contato = False
    elif escopo.get('pessoa_id') and id == escopo['pessoa_id']:
        somente_contato = True
    else:
        negar_gestao_cadastro(escopo, 'ACESSO_NEGADO_CADASTRO')
    service = PessoaService(db)
    return await service.update_pessoa(id, dto, somente_contato=somente_contato)


@router.delete('/pessoas/{id}')
async def delete_person(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> dict:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    if c_id:
        await assert_pessoa_no_escopo(db, escopo, id, c_id)
    negar_gestao_cadastro(escopo)
    service = PessoaService(db)
    return await service.delete_pessoa(id)
