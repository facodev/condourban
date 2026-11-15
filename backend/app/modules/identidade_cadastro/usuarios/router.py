import uuid
from fastapi import APIRouter, HTTPException, Query, status

from app.core.dependencies import ActiveCondominioDep, CurrentUserDep, SessionDep
from app.core.rbac import (
    assert_unidade_no_escopo,
    negar_gestao_cadastro,
    resolver_escopo_cadastro,
)
from .schemas import (
    InativarOcupacaoRequest,
    OcupacaoUnidadeCreate,
    OcupacaoUnidadeResponse,
    OcupacaoUnidadeUpdate,
    RotinaExpiracaoResponse,
    Token,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse,
    UsuarioUpdate,
)
from .service import OcupacaoUnidadeService, UsuarioService

router = APIRouter(prefix='/usuarios', tags=['Identidade - Usuários'])
ocupacoes_router = APIRouter(prefix='/ocupacoes', tags=['Identidade - Ocupações de Unidade'])


@router.get('', response_model=list[UsuarioResponse])
async def list_users(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> list[UsuarioResponse]:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = UsuarioService(db)
    return await service.list_usuarios(condominio_id=c_id)


@router.post(
    '',
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_usuario(
    dto: UsuarioCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> UsuarioResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = UsuarioService(db)
    return await service.create_usuario(dto, condominio_id=c_id)


@router.post(
    '/registrar',
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
@router.post(
    '/register',
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def register(dto: UsuarioCreate, db: SessionDep) -> UsuarioResponse:
    service = UsuarioService(db)
    return await service.create_usuario(dto)


@router.post('/login', response_model=Token)
async def login(dto: UsuarioLogin, db: SessionDep) -> Token:
    service = UsuarioService(db)
    return await service.authenticate(dto)


@router.get('/{id}', response_model=UsuarioResponse)
async def obter_usuario(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> UsuarioResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = UsuarioService(db)
    return await service.get_usuario(id)


@router.patch('/{id}', response_model=UsuarioResponse)
@router.put('/{id}', response_model=UsuarioResponse, include_in_schema=False)
async def atualizar_usuario(
    id: uuid.UUID,
    dto: UsuarioUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> UsuarioResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = UsuarioService(db)
    return await service.update_usuario(id, dto, condominio_id=c_id)


@router.delete('/{id}')
async def deletar_usuario(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> dict:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = UsuarioService(db)
    return await service.delete_usuario(id)


# ============================================================================
# Endpoints de Ocupações de Unidade
# ============================================================================


@ocupacoes_router.get('', response_model=list[OcupacaoUnidadeResponse])
async def listar_ocupacoes(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
    unidade_id: uuid.UUID | None = Query(None),
    apenas_ativas: bool = Query(False),
) -> list[OcupacaoUnidadeResponse]:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )


    escopo = await resolver_escopo_cadastro(db, current_user)
    service = OcupacaoUnidadeService(db)
    unidade_ids = None if escopo['ver_todos'] else escopo['unidade_ids']
    if unidade_id and not escopo['ver_todos']:
        await assert_unidade_no_escopo(escopo, unidade_id)
    return await service.listar_ocupacoes(
        unidade_id=unidade_id,
        condominio_id=c_id,
        apenas_ativas=apenas_ativas,
        unidade_ids=unidade_ids,
    )


@ocupacoes_router.post(
    '',
    response_model=OcupacaoUnidadeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_ocupacao(
    dto: OcupacaoUnidadeCreate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> OcupacaoUnidadeResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )


    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OcupacaoUnidadeService(db)
    return await service.criar_ocupacao(dto, condominio_id=c_id)


@ocupacoes_router.get('/{id}', response_model=OcupacaoUnidadeResponse)
async def obter_ocupacao(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> OcupacaoUnidadeResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    service = OcupacaoUnidadeService(db)
    ocupacao = await service.obter_ocupacao(id)
    if c_id and ocupacao.condominio_id != c_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='ACESSO_NEGADO_OUTRO_CONDOMINIO',
        )
    await assert_unidade_no_escopo(escopo, ocupacao.unidade_id)
    return ocupacao


@ocupacoes_router.patch('/{id}', response_model=OcupacaoUnidadeResponse)
async def atualizar_ocupacao(
    id: uuid.UUID,
    dto: OcupacaoUnidadeUpdate,
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> OcupacaoUnidadeResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OcupacaoUnidadeService(db)
    ocupacao = await service.obter_ocupacao(id)
    if c_id and ocupacao.condominio_id != c_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='ACESSO_NEGADO_OUTRO_CONDOMINIO',
        )
    return await service.atualizar_ocupacao(id, dto)


@ocupacoes_router.post('/{id}/inativar')
async def inativar_ocupacao(
    id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUserDep,
    dto: InativarOcupacaoRequest | None = None,
    condominio_id: ActiveCondominioDep = None,
) -> dict:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OcupacaoUnidadeService(db)
    ocupacao = await service.obter_ocupacao(id)
    if c_id and ocupacao.condominio_id != c_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='ACESSO_NEGADO_OUTRO_CONDOMINIO',
        )
    cascade = dto.cascade_dependentes if dto else True
    novo_resp = dto.novo_responsavel_ocupacao_id if dto else None
    return await service.inativar_ocupacao(
        id, cascade_dependentes=cascade, novo_responsavel_ocupacao_id=novo_resp
    )


@ocupacoes_router.post('/rotina-expiracao', response_model=RotinaExpiracaoResponse)
async def rotina_expiracao(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: ActiveCondominioDep = None,
) -> RotinaExpiracaoResponse:
    c_id = condominio_id or (
        uuid.UUID(current_user['condominio_id'])
        if current_user.get('condominio_id')
        else None
    )
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OcupacaoUnidadeService(db)
    return await service.executar_rotina_expiracao(c_id)
