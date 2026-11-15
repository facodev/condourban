"""Políticas de escopo RBAC para cadastros de identidade."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Consulta ampla (pode VER todos os cadastros) — inclui portaria/encomendas/conselho
PAPEIS_CONSULTA_AMPLA = frozenset(
    {
        'SUPERADMIN',
        'ADMINISTRADOR',
        'ADMIN',
        'ADMINISTRADORA',
        'SINDICO',
        'SUBSINDICO',
        'CONSELHO',
        'PORTARIA',
        'PORTEIRO',
        'ENCOMENDAS',
        'FUNCIONARIO',
        'ZELADOR',
    }
)

# Edição sensível — só síndico / administrador (e equivalentes)
# Portaria e conselho NÃO editam cadastros civis, vínculos, estrutura, etc.
PAPEIS_EDICAO_GESTAO = frozenset(
    {
        'SUPERADMIN',
        'ADMINISTRADOR',
        'ADMIN',
        'ADMINISTRADORA',
        'SINDICO',
        'SUBSINDICO',
    }
)

# Operação de correspondências (create/baixa) — distinto de liberação de entrada
PAPEIS_OPERACAO_ENCOMENDAS = frozenset(
    {
        'ENCOMENDAS',
        'ZELADOR',
        'SUPERADMIN',
        'ADMINISTRADOR',
        'ADMIN',
        'ADMINISTRADORA',
        'SINDICO',
        'SUBSINDICO',
    }
)

# Liberação de entrada / visitantes — distinto de correspondências
PAPEIS_OPERACAO_VISITANTES = frozenset(
    {
        'PORTARIA',
        'PORTEIRO',
        'SUPERADMIN',
        'ADMINISTRADOR',
        'ADMIN',
        'ADMINISTRADORA',
        'SINDICO',
        'SUBSINDICO',
    }
)

# Alias legado
PAPEIS_GESTAO_CADASTRO = PAPEIS_CONSULTA_AMPLA

STATUS_OCUPACAO_ATIVA = ('ATIVO', 'ATIVA')


def normalizar_papeis(papeis: list[str] | None) -> set[str]:
    return {str(p).upper() for p in (papeis or []) if p}


def pode_ver_todos_cadastros(papeis: list[str] | None) -> bool:
    return bool(normalizar_papeis(papeis) & PAPEIS_CONSULTA_AMPLA)


def pode_editar_cadastros(papeis: list[str] | None) -> bool:
    """Síndico/administrador — nunca portaria."""
    return bool(normalizar_papeis(papeis) & PAPEIS_EDICAO_GESTAO)


def pode_operar_encomendas(papeis: list[str] | None) -> bool:
    return bool(normalizar_papeis(papeis) & PAPEIS_OPERACAO_ENCOMENDAS)


def pode_operar_visitantes(papeis: list[str] | None) -> bool:
    return bool(normalizar_papeis(papeis) & PAPEIS_OPERACAO_VISITANTES)


def exigir_papel(
    papeis: list[str] | None,
    permitidos: frozenset[str],
    detalhe: str = 'ACESSO_NEGADO',
) -> None:
    if not (normalizar_papeis(papeis) & permitidos):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detalhe)


async def resolver_pessoa_id(
    db: AsyncSession, user_id: str | uuid.UUID
) -> uuid.UUID | None:
    from app.modules.identidade_cadastro.usuarios.models import Usuario

    try:
        uid = uuid.UUID(str(user_id))
    except (ValueError, TypeError):
        return None
    user = (
        await db.execute(select(Usuario).where(Usuario.id == uid))
    ).scalar_one_or_none()
    return user.pessoa_id if user else None


async def unidades_ativas_da_pessoa(
    db: AsyncSession, pessoa_id: uuid.UUID
) -> list[uuid.UUID]:
    from app.modules.identidade_cadastro.usuarios.models import OcupacaoUnidade

    rows = (
        await db.execute(
            select(OcupacaoUnidade.unidade_id).where(
                OcupacaoUnidade.pessoa_id == pessoa_id,
                OcupacaoUnidade.status.in_(STATUS_OCUPACAO_ATIVA),
            )
        )
    ).scalars().all()
    return list({u for u in rows if u})


async def pessoa_ids_nas_unidades(
    db: AsyncSession, unidade_ids: list[uuid.UUID]
) -> list[uuid.UUID]:
    from app.modules.identidade_cadastro.usuarios.models import OcupacaoUnidade

    if not unidade_ids:
        return []
    rows = (
        await db.execute(
            select(OcupacaoUnidade.pessoa_id).where(
                OcupacaoUnidade.unidade_id.in_(unidade_ids),
                OcupacaoUnidade.status.in_(STATUS_OCUPACAO_ATIVA),
            )
        )
    ).scalars().all()
    return list({p for p in rows if p})


async def resolver_escopo_cadastro(
    db: AsyncSession, current_user: dict
) -> dict:
    """Metadados de escopo para identidade / estrutura.

    - ver_todos: consulta ampla (gestão + portaria + conselho)
    - pode_editar: mutações sensíveis (só síndico/admin)
    - pessoa_id / unidade_ids: escopo do morador
    """
    papeis = current_user.get('papeis') or []
    ver_todos = pode_ver_todos_cadastros(papeis)
    pode_editar = pode_editar_cadastros(papeis)
    pessoa_id = await resolver_pessoa_id(db, current_user['user_id'])
    unidade_ids: list[uuid.UUID] = []
    if pessoa_id and not ver_todos:
        unidade_ids = await unidades_ativas_da_pessoa(db, pessoa_id)
    elif pessoa_id and not pode_editar:
        # Portaria: ainda resolve unidades próprias (contato pessoal)
        unidade_ids = await unidades_ativas_da_pessoa(db, pessoa_id)
    return {
        'ver_todos': ver_todos,
        'pode_editar': pode_editar,
        'pessoa_id': pessoa_id,
        'unidade_ids': unidade_ids,
        'papeis': list(normalizar_papeis(papeis)),
    }


def negar_gestao_cadastro(
    escopo: dict, detalhe: str = 'ACESSO_NEGADO_CADASTRO'
) -> None:
    """Bloqueia mutação se não for síndico/administrador."""
    if not escopo.get('pode_editar'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detalhe)


async def assert_pessoa_no_escopo(
    db: AsyncSession,
    escopo: dict,
    pessoa_id: uuid.UUID,
    condominio_id: uuid.UUID | None = None,
) -> None:
    """Garante que a pessoa pertença ao condomínio ativo ou seja a própria pessoa."""
    if not condominio_id:
        c_info = db.info.get('condominio_id')
        if c_info:
            try:
                condominio_id = uuid.UUID(str(c_info))
            except (ValueError, TypeError):
                pass

    propria = escopo.get('pessoa_id')
    if propria and pessoa_id == propria:
        return

    permitidas = set(await ids_pessoas_visiveis(db, escopo, condominio_id))
    if propria:
        permitidas.add(propria)
    if pessoa_id not in permitidas:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='ACESSO_NEGADO_FORA_DO_CONDOMINIO',
        )


async def assert_unidade_no_escopo(
    escopo: dict, unidade_id: uuid.UUID, *, escrita: bool = False
) -> None:
    """Leitura: ver_todos ou própria unidade.
    Escrita: só gestão (pode_editar) ou própria unidade do morador.
    """
    if escrita:
        if escopo.get('pode_editar'):
            return
        if unidade_id in set(escopo.get('unidade_ids') or []):
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='ACESSO_NEGADO_FORA_DA_UNIDADE',
        )
    if escopo.get('ver_todos'):
        return
    if unidade_id not in set(escopo.get('unidade_ids') or []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='ACESSO_NEGADO_FORA_DA_UNIDADE',
        )


async def ids_pessoas_visiveis(
    db: AsyncSession,
    escopo: dict,
    condominio_id: uuid.UUID | None = None,
) -> list[uuid.UUID]:
    """Retorna IDs das pessoas acessíveis no escopo do condomínio ativo.
    Nunca retorna None (sem filtro) para evitar vazamento cross-tenant de pessoas.
    """
    from app.modules.identidade_cadastro.usuarios.models import (
        MembroCondominio,
        OcupacaoUnidade,
    )

    if not condominio_id:
        c_info = db.info.get('condominio_id')
        if c_info:
            try:
                condominio_id = uuid.UUID(str(c_info))
            except (ValueError, TypeError):
                pass

    if not condominio_id:
        return []

    if escopo.get('ver_todos'):
        # Todos do condomínio ativo via membro_condominio ou ocupacao_unidade
        m_stmt = select(MembroCondominio.pessoa_id).where(
            MembroCondominio.condominio_id == condominio_id,
            MembroCondominio.status == 'ATIVO',
        )
        o_stmt = select(OcupacaoUnidade.pessoa_id).where(
            OcupacaoUnidade.condominio_id == condominio_id,
            OcupacaoUnidade.status.in_(STATUS_OCUPACAO_ATIVA),
        )
        m_ids = (await db.execute(m_stmt)).scalars().all()
        o_ids = (await db.execute(o_stmt)).scalars().all()
        return list({p for p in (list(m_ids) + list(o_ids)) if p})

    # Escopo restrito a morador: pessoas nas unidades autorizadas
    ids = set(await pessoa_ids_nas_unidades(db, escopo.get('unidade_ids') or []))
    if escopo.get('pessoa_id'):
        ids.add(escopo['pessoa_id'])
    return list(ids)
