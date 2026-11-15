import uuid
from fastapi import APIRouter, Query, status

from app.core.dependencies import CurrentUserDep, SessionDep
from app.core.rbac import negar_gestao_cadastro, resolver_escopo_cadastro
from .schemas import (
    AprovarSolicitacaoRequest,
    ConfirmarMagicLinkRequest,
    ConfirmarMagicLinkResponse,
    ConviteEnvioRequest,
    ConviteEnvioResponse,
    RejeitarSolicitacaoRequest,
    RevogarVinculoRequest,
    RevogarVinculoResponse,
    SolicitacaoAprovacaoResponse,
    SolicitacaoCadastroResponse,
    SolicitacaoIngressoRequest,
    SolicitacaoRejeicaoResponse,
    VerificarCpfOnboardingRequest,
    VerificarCpfOnboardingResponse,
)
from .service import OnboardingService

router = APIRouter(tags=['Identidade - Onboarding e Convites'])


@router.post(
    '/convites',
    response_model=ConviteEnvioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_convite(
    dto: ConviteEnvioRequest,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> ConviteEnvioResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OnboardingService(db)
    return await service.criar_convite(dto)


@router.post(
    '/convites/{token}/aceitar',
    status_code=status.HTTP_200_OK,
)
async def aceitar_convite(
    token: str,
    db: SessionDep,
) -> dict:
    service = OnboardingService(db)
    return await service.aceitar_convite(token)


@router.post(
    '/onboarding/solicitar',
    response_model=SolicitacaoCadastroResponse,
    status_code=status.HTTP_201_CREATED,
)
async def solicitar_onboarding(
    dto: SolicitacaoIngressoRequest,
    db: SessionDep,
) -> SolicitacaoCadastroResponse:
    service = OnboardingService(db)
    return await service.solicitar_cadastro(dto)


@router.get(
    '/onboarding/solicitacoes',
    response_model=list[SolicitacaoCadastroResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_solicitacoes(
    db: SessionDep,
    current_user: CurrentUserDep,
    condominio_id: uuid.UUID | None = Query(None),
    status: str | None = Query(None),
) -> list[SolicitacaoCadastroResponse]:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OnboardingService(db)
    return await service.listar_solicitacoes(
        condominio_id=condominio_id,
        status_filtro=status,
    )


@router.post(
    '/onboarding/solicitacoes/{id}/aprovar',
    response_model=SolicitacaoAprovacaoResponse,
    status_code=status.HTTP_200_OK,
)
@router.post(
    '/onboarding/{id}/aprovar',
    response_model=SolicitacaoAprovacaoResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def aprovar_solicitacao(
    id: uuid.UUID,
    dto: AprovarSolicitacaoRequest,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> SolicitacaoAprovacaoResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OnboardingService(db)
    return await service.aprovar_solicitacao(id, dto)


@router.post(
    '/onboarding/solicitacoes/{id}/rejeitar',
    response_model=SolicitacaoRejeicaoResponse,
    status_code=status.HTTP_200_OK,
)
@router.post(
    '/onboarding/{id}/rejeitar',
    response_model=SolicitacaoRejeicaoResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def rejeitar_solicitacao(
    id: uuid.UUID,
    dto: RejeitarSolicitacaoRequest,
    db: SessionDep,
    current_user: CurrentUserDep,
) -> SolicitacaoRejeicaoResponse:
    escopo = await resolver_escopo_cadastro(db, current_user)
    negar_gestao_cadastro(escopo)
    service = OnboardingService(db)
    return await service.rejeitar_solicitacao(id, dto)


@router.post(
    '/onboarding/verificar-cpf',
    response_model=VerificarCpfOnboardingResponse,
    status_code=status.HTTP_200_OK,
)
async def verificar_cpf_onboarding(
    dto: VerificarCpfOnboardingRequest,
    db: SessionDep,
) -> VerificarCpfOnboardingResponse:
    service = OnboardingService(db)
    return await service.verificar_cpf_onboarding(dto)


@router.post(
    '/onboarding/confirmar-magic-link',
    response_model=ConfirmarMagicLinkResponse,
    status_code=status.HTTP_200_OK,
)
async def confirmar_magic_link(
    dto: ConfirmarMagicLinkRequest,
    db: SessionDep,
) -> ConfirmarMagicLinkResponse:
    service = OnboardingService(db)
    return await service.confirmar_magic_link(dto)


@router.post(
    '/onboarding/revogar-vinculo',
    response_model=RevogarVinculoResponse,
    status_code=status.HTTP_200_OK,
)
async def revogar_vinculo(
    dto: RevogarVinculoRequest,
    db: SessionDep,
) -> RevogarVinculoResponse:
    service = OnboardingService(db)
    return await service.revogar_vinculo(dto)


@router.get(
    '/onboarding/revogar-vinculo',
    response_model=RevogarVinculoResponse,
    status_code=status.HTTP_200_OK,
)
async def revogar_vinculo_get(
    token: str,
    db: SessionDep,
) -> RevogarVinculoResponse:
    service = OnboardingService(db)
    return await service.revogar_vinculo(RevogarVinculoRequest(token=token))
