import asyncio
import base64
import hashlib
import sys
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# Garantir que a pasta backend esteja no sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, func

# Importar todos os modelos para registro completo no Base.metadata
import app.modules.identidade_cadastro.pessoas.models  # noqa
import app.modules.identidade_cadastro.usuarios.models  # noqa
import app.modules.identidade_cadastro.onboarding.models  # noqa
import app.modules.identidade_cadastro.veiculos_pets.models  # noqa
import app.modules.condominio.branding.models  # noqa
import app.modules.condominio.blocos_unidades.models  # noqa
import app.modules.condominio.vagas.models  # noqa
import app.modules.condominio.estrutura.models  # noqa
import app.modules.condominio.areas_comuns.models  # noqa
import app.modules.controle_acesso.dispositivos.models  # noqa
import app.modules.controle_acesso.credenciais.models  # noqa
import app.modules.controle_acesso.eventos_acesso.models  # noqa
import app.modules.portaria.atendimento.models  # noqa
import app.modules.portaria.encomendas.models  # noqa
import app.modules.reservas.agendamentos.models  # noqa
import app.modules.reservas.vistorias.models  # noqa
import app.modules.comunicacao.mensageria.models  # noqa
import app.modules.comunicacao.ocorrencias.models  # noqa
import app.modules.comunicacao.mural_social.models  # noqa
import app.modules.governanca.assembleias.models  # noqa
import app.modules.governanca.seguranca_auditoria.models  # noqa
import app.modules.financeiro.cobrancas_acordos.models  # noqa
import app.modules.financeiro.despesas_medicoes.models  # noqa
import app.modules.manutencao.chamados_servicos.models  # noqa
import app.modules.manutencao.plano_inventario.models  # noqa

from app.core.database import async_session_maker, engine, Base
from app.core.security import get_password_hash
from app.modules.condominio.estrutura.models import Inquilino, Condominio, Bloco, Unidade, VagaGaragem
from app.modules.condominio.areas_comuns.models import AreaComum
from app.modules.identidade_cadastro.pessoas.models import Pessoa, DocumentoIdentificacao
from app.modules.identidade_cadastro.usuarios.models import Usuario, MembroCondominio, OcupacaoUnidade
from app.modules.identidade_cadastro.onboarding.models import (
    ConviteCadastroMorador,
    SolicitacaoCadastroMorador,
    DocumentoCadastro,
    VerificacaoFacial,
)
from app.modules.identidade_cadastro.veiculos_pets.models import Veiculo, Pet


def processar_cpf_seed(cpf_num: str) -> tuple[str, str]:
    cpf_limpo = cpf_num.replace(".", "").replace("-", "").strip()
    c_hash = hashlib.sha256(cpf_limpo.encode("utf-8")).hexdigest()
    c_crip = base64.b64encode(cpf_limpo.encode("utf-8")).decode("utf-8")
    return c_hash, c_crip


async def seed():
    print("Iniciando seed completo do banco de dados CondoUrban...")

    # 0. Criar todas as tabelas no banco de dados ativo (PostgreSQL em dev / SQLite em testes)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        # =========================================================================
        # SEÇÃO 1: BC CONDOMÍNIO (ESTRUTURA, BRANDING, BLOCOS, UNIDADES, VAGAS, ÁREAS)
        # =========================================================================

        # 1.1 Inquilino Mantenedor do SaaS
        res = await session.execute(select(Inquilino).limit(1))
        inquilino = res.scalar_one_or_none()
        if not inquilino:
            inquilino = Inquilino(
                id=uuid.uuid4(),
                nome="CondoUrban Gestão e Tecnologia SaaS",
                nome_fantasia="CondoUrban",
                documento="12.345.678/0001-90",
                status="ATIVO",
            )
            session.add(inquilino)
            await session.flush()
            print(f"Inquilino SaaS: {inquilino.nome}")

        # 1.2 Condomínios de Referência
        condominios_data = [
            {
                "nome": "Condomínio Residencial Jardins",
                "razao_social": "Condomínio Residencial Jardins SPE",
                "cnpj": "98.765.432/0001-10",
                "cep": "01310-100",
                "logradouro": "Avenida Paulista",
                "numero": "1000",
                "complemento": "Edifício Residencial Jardins",
                "bairro": "Bela Vista",
                "cidade": "São Paulo",
                "uf": "SP",
                "branding": {
                    "cor_primaria": "#1e40af",
                    "cor_secundaria": "#0284c7",
                    "tema": "modern",
                    "logo_url": "/assets/branding/jardins-logo.svg",
                },
                "regras_operacionais": {
                    "silencio_inicio": "22:00",
                    "silencio_fim": "08:00",
                    "mudancas_permitidas": ["SEGUNDA_A_SEXTA_08_17", "SABADO_08_12"],
                },
            },
            {
                "nome": "Residencial Solar das Acácias",
                "razao_social": "Condomínio Solar das Acácias",
                "cnpj": "45.123.890/0001-55",
                "cep": "70070-120",
                "logradouro": "SHCS Quadra 302 Bloco B",
                "numero": "S/N",
                "complemento": "Superquadra",
                "bairro": "Asa Sul",
                "cidade": "Brasília",
                "uf": "DF",
                "branding": {
                    "cor_primaria": "#059669",
                    "tema": "classic",
                },
                "regras_operacionais": {
                    "silencio_inicio": "22:00",
                    "silencio_fim": "08:00",
                },
            },
            {
                "nome": "Edifício Metropolitan Tower",
                "razao_social": "Condomínio Metropolitan Tower",
                "cnpj": "33.987.654/0001-22",
                "cep": "22041-001",
                "logradouro": "Avenida Atlântica",
                "numero": "2400",
                "complemento": "Posto 4",
                "bairro": "Copacabana",
                "cidade": "Rio de Janeiro",
                "uf": "RJ",
                "branding": {
                    "cor_primaria": "#d97706",
                    "tema": "luxury",
                },
                "regras_operacionais": {
                    "silencio_inicio": "22:00",
                    "silencio_fim": "08:00",
                },
            },
        ]

        condos_map = {}
        for c_data in condominios_data:
            res_c = await session.execute(select(Condominio).where(Condominio.nome == c_data["nome"]))
            c_obj = res_c.scalar_one_or_none()
            if not c_obj:
                c_obj = Condominio(
                    id=uuid.uuid4(),
                    inquilino_id=inquilino.id,
                    nome=c_data["nome"],
                    razao_social=c_data["razao_social"],
                    cnpj=c_data["cnpj"],
                    cep=c_data["cep"],
                    logradouro=c_data["logradouro"],
                    numero=c_data["numero"],
                    complemento=c_data["complemento"],
                    bairro=c_data["bairro"],
                    cidade=c_data["cidade"],
                    uf=c_data["uf"],
                    status="ATIVO",
                    configuracoes={
                        "branding": c_data["branding"],
                        "regras_operacionais": c_data["regras_operacionais"],
                    },
                )
                session.add(c_obj)
                await session.flush()
                print(f"Condomínio criado: {c_obj.nome}")
            condos_map[c_data["nome"]] = c_obj

        condo_principal = condos_map["Condomínio Residencial Jardins"]

        # 1.3 Blocos no Condomínio Principal
        blocos_data = [
            {"nome": "Bloco A - Girassol", "descricao": "Torre residencial frontal com 12 andares", "ordem": 1},
            {"nome": "Bloco B - Orquídea", "descricao": "Torre residencial central com 10 andares", "ordem": 2},
            {"nome": "Bloco C - Tulipa", "descricao": "Torre com unidades duplex e coberturas", "ordem": 3},
        ]

        blocos_map = {}
        for b_data in blocos_data:
            res_b = await session.execute(
                select(Bloco).where(Bloco.condominio_id == condo_principal.id, Bloco.nome == b_data["nome"])
            )
            bloco_obj = res_b.scalar_one_or_none()
            if not bloco_obj:
                bloco_obj = Bloco(
                    id=uuid.uuid4(),
                    condominio_id=condo_principal.id,
                    nome=b_data["nome"],
                    descricao=b_data["descricao"],
                    ordem=b_data["ordem"],
                    status="ATIVO",
                )
                session.add(bloco_obj)
                await session.flush()
            blocos_map[b_data["nome"]] = bloco_obj

        # Blocos no segundo condomínio (Solar das Acácias)
        condo_acacias = condos_map["Residencial Solar das Acácias"]
        for b_nome in ["Torre Norte", "Torre Sul"]:
            res_b = await session.execute(
                select(Bloco).where(Bloco.condominio_id == condo_acacias.id, Bloco.nome == b_nome)
            )
            if not res_b.scalar_one_or_none():
                session.add(Bloco(id=uuid.uuid4(), condominio_id=condo_acacias.id, nome=b_nome, status="ATIVO"))
        await session.flush()

        # 1.4 Unidades Habitacionais no Condomínio Principal
        unidades_seed = [
            ("Bloco A - Girassol", "Apt 101", 1, "APARTAMENTO", "Unidade lateral sol da manhã", 85.5),
            ("Bloco A - Girassol", "Apt 102", 1, "APARTAMENTO", "Unidade lateral sol da tarde", 85.5),
            ("Bloco A - Girassol", "Apt 201", 2, "APARTAMENTO", "Unidade frontal vista jardins", 92.0),
            ("Bloco A - Girassol", "Apt 202", 2, "APARTAMENTO", "Unidade frontal vista boulevard", 92.0),
            ("Bloco A - Girassol", "Apt 301", 3, "APARTAMENTO", "Unidade reformada 3 quartos", 110.0),
            ("Bloco B - Orquídea", "Apt 101", 1, "APARTAMENTO", "Unidade 2 quartos compacta", 78.0),
            ("Bloco B - Orquídea", "Apt 102", 1, "APARTAMENTO", "Unidade térrea com quintal privativo", 95.0),
            ("Bloco B - Orquídea", "Apt 201", 2, "APARTAMENTO", "Unidade 2 quartos padrão", 80.0),
            ("Bloco B - Orquídea", "Cobertura 501", 5, "COBERTURA", "Cobertura duplex com piscina e churrasqueira", 180.0),
            ("Bloco C - Tulipa", "Duplex 101", 1, "DUPLEX", "Unidade duplex pé direito duplo", 145.0),
        ]

        unidades_map = {}
        for b_nome, ident, andar, tipo, descr, area in unidades_seed:
            bloco_id = blocos_map[b_nome].id
            res_u = await session.execute(
                select(Unidade).where(Unidade.bloco_id == bloco_id, Unidade.identificacao == ident)
            )
            u_obj = res_u.scalar_one_or_none()
            if not u_obj:
                u_obj = Unidade(
                    id=uuid.uuid4(),
                    condominio_id=condo_principal.id,
                    bloco_id=bloco_id,
                    identificacao=ident,
                    andar=andar,
                    tipo=tipo,
                    descricao=descr,
                    area_privativa=area,
                    status="ATIVO",
                )
                session.add(u_obj)
                await session.flush()
            unidades_map[f"{b_nome}_{ident}"] = u_obj

        # 1.5 Vagas de Garagem Demarcadas
        vagas_data = [
            ("G-01", "CARRO", True, "Bloco A - Girassol_Apt 101"),
            ("G-02", "CARRO", True, "Bloco A - Girassol_Apt 102"),
            ("G-03", "CARRO", True, "Bloco A - Girassol_Apt 201"),
            ("G-04", "CARRO", False, "Bloco B - Orquídea_Apt 101"),
            ("G-05", "CARRO", True, "Bloco B - Orquídea_Cobertura 501"),
            ("G-06", "CARRO", True, "Bloco C - Tulipa_Duplex 101"),
            ("M-01", "MOTO", True, "Bloco A - Girassol_Apt 101"),
            ("M-02", "MOTO", False, None),
            ("PCD-01", "PCD", True, None),
            ("VIS-01", "VISITANTE", False, None),
            ("VIS-02", "VISITANTE", False, None),
        ]

        for ident, tipo, coberta, u_key in vagas_data:
            res_v = await session.execute(
                select(VagaGaragem).where(
                    VagaGaragem.condominio_id == condo_principal.id, VagaGaragem.identificacao == ident
                )
            )
            if not res_v.scalar_one_or_none():
                unid_id = unidades_map[u_key].id if u_key and u_key in unidades_map else None
                session.add(
                    VagaGaragem(
                        id=uuid.uuid4(),
                        condominio_id=condo_principal.id,
                        unidade_id=unid_id,
                        identificacao=ident,
                        tipo=tipo,
                        coberta=coberta,
                        status="ATIVO",
                    )
                )
        await session.flush()

        # 1.6 Áreas Comuns e Espaços Compartilhados
        areas_data = [
            {
                "nome": "Salão de Festas Nobre",
                "descricao": "Espaço climatizado com cozinha completa, mesas e sonorização embutida.",
                "capacidade": 120,
                "taxa_reserva": 150.0,
                "abertura": "09:00",
                "fechamento": "02:00",
            },
            {
                "nome": "Espaço Gourmet com Churrasqueira",
                "descricao": "Churrasqueira gourmet, forno de pizza e cervejeira para encontros familiares.",
                "capacidade": 45,
                "taxa_reserva": 80.0,
                "abertura": "10:00",
                "fechamento": "23:00",
            },
            {
                "nome": "Piscina Semi-Olímpica Climatizada",
                "descricao": "Piscina aquecida para práticas esportivas e lazer, com deck molhado e solarium.",
                "capacidade": 60,
                "taxa_reserva": 0.0,
                "abertura": "07:00",
                "fechamento": "21:00",
            },
            {
                "nome": "Academia & Centro Fitness",
                "descricao": "Aparelhos modernos para musculação, esteiras ergométricas e espaço para pilates.",
                "capacidade": 30,
                "taxa_reserva": 0.0,
                "abertura": "06:00",
                "fechamento": "23:00",
            },
            {
                "nome": "Quadra Poliesportiva",
                "descricao": "Piso modular para futsal, basquete e vôlei com iluminação em LED.",
                "capacidade": 25,
                "taxa_reserva": 0.0,
                "abertura": "08:00",
                "fechamento": "22:00",
            },
            {
                "nome": "Espaço Coworking & Sala de Reunião",
                "descricao": "Bancadas de trabalho individual, Wi-Fi 6 de alta velocidade e TV para apresentações.",
                "capacidade": 16,
                "taxa_reserva": 0.0,
                "abertura": "07:00",
                "fechamento": "22:00",
            },
        ]

        for a_data in areas_data:
            res_a = await session.execute(
                select(AreaComum).where(
                    AreaComum.condominio_id == condo_principal.id, AreaComum.nome == a_data["nome"]
                )
            )
            if not res_a.scalar_one_or_none():
                session.add(
                    AreaComum(
                        id=uuid.uuid4(),
                        condominio_id=condo_principal.id,
                        nome=a_data["nome"],
                        descricao=a_data["descricao"],
                        capacidade=a_data["capacidade"],
                        taxa_reserva=a_data["taxa_reserva"],
                        horario_abertura=a_data["abertura"],
                        horario_fechamento=a_data["fechamento"],
                        requer_aprovacao=True,
                        ativo=True,
                    )
                )
        await session.flush()

        # =========================================================================
        # SEÇÃO 2: BC IDENTIDADE E CADASTRO (PESSOAS, USUÁRIOS, RBAC, OCUPAÇÕES, ONBOARDING, VEÍCULOS, PETS)
        # =========================================================================

        # 2.1 Usuários de Sistema e Membresias RBAC
        senha_hash_padrao = get_password_hash("admin123")

        usuarios_seed = [
            {
                "email": "admin@condourban.com",
                "nome": "Super Administrador",
                "papel": "SUPERADMIN",
                "cpf": "000.111.222-33",
                "rg": "11.222.333-X",
                "celular": "11999990000",
            },
            {
                "email": "sindico@condourban.com",
                "nome": "Carlos Eduardo Silva",
                "papel": "ADMINISTRADOR",
                "cpf": "111.222.333-44",
                "rg": "22.333.444-5",
                "celular": "11988881111",
            },
            {
                "email": "portaria@condourban.com",
                "nome": "José da Guarita",
                "papel": "PORTARIA",
                "cpf": "222.333.444-55",
                "rg": "33.444.555-6",
                "celular": "11977772222",
            },
            {
                "email": "encomendas@condourban.com",
                "nome": "Ana Correspondências",
                "papel": "ENCOMENDAS",
                "cpf": "222.333.444-56",
                "rg": "33.444.555-7",
                "celular": "11977772223",
            },
            {
                "email": "morador@condourban.com",
                "nome": "Mariana Costa Ferreira",
                "papel": "MORADOR",
                "cpf": "333.444.555-66",
                "rg": "44.555.666-8",
                "celular": "11966663333",
            },
            {
                "email": "conselho@condourban.com",
                "nome": "Roberto Alencar Mendes",
                "papel": "CONSELHO",
                "cpf": "444.555.666-77",
                "rg": "55.666.777-9",
                "celular": "11955554444",
            },
            {
                "email": "zelador@condourban.com",
                "nome": "Sebastião Oliveira",
                "papel": "FUNCIONARIO",
                "cpf": "555.666.777-80",
                "rg": "66.777.888-0",
                "celular": "11955553333",
            },
        ]

        pessoas_usuarios_map = {}
        for u_data in usuarios_seed:
            res_u = await session.execute(select(Usuario).where(Usuario.email == u_data["email"]))
            user = res_u.scalar_one_or_none()
            if not user:
                c_hash, c_crip = processar_cpf_seed(u_data["cpf"])
                pessoa = Pessoa(
                    id=uuid.uuid4(),
                    inquilino_id=inquilino.id,
                    nome_completo=u_data["nome"],
                    email=u_data["email"],
                    celular=u_data["celular"],
                    cpf_hash=c_hash,
                    cpf_criptografado=c_crip,
                    data_nascimento=date(1985, 5, 20),
                    status="ATIVO",
                )
                session.add(pessoa)
                await session.flush()

                # Documento civil vinculado
                session.add(
                    DocumentoIdentificacao(
                        id=uuid.uuid4(),
                        pessoa_id=pessoa.id,
                        tipo="RG",
                        numero=u_data["rg"],
                        orgao_emissor="SSP",
                        uf="SP",
                    )
                )

                user = Usuario(
                    id=uuid.uuid4(),
                    pessoa_id=pessoa.id,
                    email=u_data["email"],
                    senha_hash=senha_hash_padrao,
                    email_verificado=True,
                    status="ATIVO",
                )
                session.add(user)
                await session.flush()

                # Membresia no condomínio (mapeamento civil ADR-008)
                mapa_tipo_civil = {
                    "SUPERADMIN": "ADMINISTRADOR",
                    "ADMINISTRADOR": "ADMINISTRADOR",
                    "SINDICO": "ADMINISTRADOR",
                    "PORTARIA": "FUNCIONARIO",
                    "ENCOMENDAS": "FUNCIONARIO",
                    "FUNCIONARIO": "FUNCIONARIO",
                    "CONSELHO": "MORADOR",
                    "MORADOR": "MORADOR",
                }
                tipo_civil = mapa_tipo_civil.get(u_data["papel"], "MORADOR")

                if u_data["papel"] == "SUPERADMIN":
                    for c_inst in condos_map.values():
                        session.add(
                            MembroCondominio(
                                id=uuid.uuid4(),
                                condominio_id=c_inst.id,
                                pessoa_id=pessoa.id,
                                tipo_pessoa="ADMINISTRADOR",
                                status="ATIVO",
                            )
                        )
                else:
                    session.add(
                        MembroCondominio(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            pessoa_id=pessoa.id,
                            tipo_pessoa=tipo_civil,
                            status="ATIVO",
                        )
                    )
                pessoas_usuarios_map[u_data["email"]] = pessoa
                print(f"Usuário criado: {u_data['email']} ({u_data['papel']})")
            else:
                p_obj = (await session.execute(select(Pessoa).where(Pessoa.email == u_data["email"]))).scalar_one_or_none()
                pessoas_usuarios_map[u_data["email"]] = p_obj

        # 2.2 Pessoas Civis Adicionais (Inquilinos, Dependentes, Locadores)
        pessoas_adicionais = [
            ("Beatriz Albuquerque", "beatriz.alb@email.com", "555.666.777-88", "11944445555", "RG", "77.888.999-1"),
            ("Fernando Meireles", "fernando.meir@email.com", "666.777.888-99", "11933336666", "CNH", "01234567890"),
            ("Camila Ramos", "camila.ramos@email.com", "777.888.999-00", "11922227777", "RG", "88.999.000-2"),
            ("Lucas Ramos (Dependente)", "lucas.ramos@email.com", "888.999.000-11", "11911118888", "RG", "99.000.111-3"),
            ("Gabriel Nogueira", "gabriel.nog@email.com", "999.000.111-22", "11900009999", "CNH", "09876543210"),
            ("Renato Silveira (Candidato Onboarding)", "renato.silveira@email.com", "123.456.789-09", "11976543210", "RG", "54.321.098-7"),
        ]

        pessoas_civis = {}
        for nome, email, cpf, cel, doc_tipo, doc_num in pessoas_adicionais:
            res_p = await session.execute(select(Pessoa).where(Pessoa.email == email))
            p_obj = res_p.scalar_one_or_none()
            if not p_obj:
                c_hash, c_crip = processar_cpf_seed(cpf)
                p_obj = Pessoa(
                    id=uuid.uuid4(),
                    inquilino_id=inquilino.id,
                    nome_completo=nome,
                    email=email,
                    celular=cel,
                    cpf_hash=c_hash,
                    cpf_criptografado=c_crip,
                    data_nascimento=date(1990, 8, 15),
                    status="ATIVO",
                )
                session.add(p_obj)
                await session.flush()

                session.add(
                    DocumentoIdentificacao(
                        id=uuid.uuid4(),
                        pessoa_id=p_obj.id,
                        tipo=doc_tipo,
                        numero=doc_num,
                        orgao_emissor="DETRAN" if doc_tipo == "CNH" else "SSP",
                        uf="SP",
                    )
                )
            pessoas_civis[nome] = p_obj
        await session.flush()

        # 2.3 Ocupações de Unidade (Validando Regras Invariantes do Domínio)
        u_101 = unidades_map.get("Bloco A - Girassol_Apt 101")
        u_102 = unidades_map.get("Bloco A - Girassol_Apt 102")
        u_201 = unidades_map.get("Bloco A - Girassol_Apt 201")
        u_cob = unidades_map.get("Bloco B - Orquídea_Cobertura 501")

        # Regra: Proprietário Residente Apt 101
        if u_101:
            p_mariana = pessoas_usuarios_map.get("morador@condourban.com")
            if p_mariana:
                res_oc = await session.execute(
                    select(OcupacaoUnidade).where(
                        OcupacaoUnidade.unidade_id == u_101.id, OcupacaoUnidade.pessoa_id == p_mariana.id
                    )
                )
                if not res_oc.scalar_one_or_none():
                    session.add(
                        OcupacaoUnidade(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            unidade_id=u_101.id,
                            pessoa_id=p_mariana.id,
                            tipo_vinculo="PROPRIETARIO",
                            mora_no_local=True,
                            principal=True,
                            inicio_em=datetime.now(timezone.utc) - timedelta(days=365),
                            status="ATIVO",
                        )
                    )

        # Regra: Inquilino Residente e Dependente Órfão Controlado Apt 102
        if u_102 and "Beatriz Albuquerque" in pessoas_civis:
            p_bia = pessoas_civis["Beatriz Albuquerque"]
            res_oc = await session.execute(
                select(OcupacaoUnidade).where(
                    OcupacaoUnidade.unidade_id == u_102.id, OcupacaoUnidade.pessoa_id == p_bia.id
                )
            )
            oc_bia = res_oc.scalar_one_or_none()
            if not oc_bia:
                oc_bia = OcupacaoUnidade(
                    id=uuid.uuid4(),
                    condominio_id=condo_principal.id,
                    unidade_id=u_102.id,
                    pessoa_id=p_bia.id,
                    tipo_vinculo="INQUILINO",
                    mora_no_local=True,
                    principal=True,
                    inicio_em=datetime.now(timezone.utc) - timedelta(days=90),
                    fim_em=datetime.now(timezone.utc) + timedelta(days=275),
                    status="ATIVO",
                )
                session.add(oc_bia)
                await session.flush()

            # Dependente vinculado ao titular responsável
            if "Lucas Ramos (Dependente)" in pessoas_civis:
                p_lucas = pessoas_civis["Lucas Ramos (Dependente)"]
                res_dep = await session.execute(
                    select(OcupacaoUnidade).where(
                        OcupacaoUnidade.unidade_id == u_102.id, OcupacaoUnidade.pessoa_id == p_lucas.id
                    )
                )
                if not res_dep.scalar_one_or_none():
                    session.add(
                        OcupacaoUnidade(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            unidade_id=u_102.id,
                            pessoa_id=p_lucas.id,
                            tipo_vinculo="DEPENDENTE",
                            mora_no_local=True,
                            responsavel_ocupacao_id=oc_bia.id,
                            inicio_em=datetime.now(timezone.utc) - timedelta(days=90),
                            status="ATIVO",
                        )
                    )

        # Regra: Locador Investidor Não Residente (mora_no_local = False) Apt 201
        if u_201 and "Fernando Meireles" in pessoas_civis:
            p_fernando = pessoas_civis["Fernando Meireles"]
            res_oc = await session.execute(
                select(OcupacaoUnidade).where(
                    OcupacaoUnidade.unidade_id == u_201.id, OcupacaoUnidade.pessoa_id == p_fernando.id
                )
            )
            if not res_oc.scalar_one_or_none():
                session.add(
                    OcupacaoUnidade(
                        id=uuid.uuid4(),
                        condominio_id=condo_principal.id,
                        unidade_id=u_201.id,
                        pessoa_id=p_fernando.id,
                        tipo_vinculo="PROPRIETARIO",
                        mora_no_local=False,
                        principal=True,
                        inicio_em=datetime.now(timezone.utc) - timedelta(days=500),
                        status="ATIVO",
                    )
                )

        # Cobertura 501: Proprietário e Conselheiro Residente
        if u_cob:
            p_conselho = pessoas_usuarios_map.get("conselho@condourban.com")
            if p_conselho:
                res_oc = await session.execute(
                    select(OcupacaoUnidade).where(
                        OcupacaoUnidade.unidade_id == u_cob.id, OcupacaoUnidade.pessoa_id == p_conselho.id
                    )
                )
                if not res_oc.scalar_one_or_none():
                    session.add(
                        OcupacaoUnidade(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            unidade_id=u_cob.id,
                            pessoa_id=p_conselho.id,
                            tipo_vinculo="PROPRIETARIO",
                            mora_no_local=True,
                            principal=True,
                            inicio_em=datetime.now(timezone.utc) - timedelta(days=200),
                            status="ATIVO",
                        )
                    )
        await session.flush()

        # 2.4 Fluxo de Onboarding e Auto-Cadastro (Convites, Solicitações, Documentos, Biometria)
        u_301 = unidades_map.get("Bloco A - Girassol_Apt 301")
        if u_301:
            # Convite ativo gerado pela administração
            res_conv = await session.execute(
                select(ConviteCadastroMorador).where(
                    ConviteCadastroMorador.condominio_id == condo_principal.id,
                    ConviteCadastroMorador.unidade_id == u_301.id,
                )
            )
            convite_301 = res_conv.scalar_one_or_none()
            if not convite_301:
                convite_301 = ConviteCadastroMorador(
                    id=uuid.uuid4(),
                    condominio_id=condo_principal.id,
                    unidade_id=u_301.id,
                    tipo_vinculo="MORADOR",
                    codigo="CONV-301",
                    token_hash="token_convite_apt_301_seguro",
                    validade_em=datetime.now(timezone.utc) + timedelta(days=15),
                    status="ATIVO",
                )
                session.add(convite_301)
                await session.flush()

            # Solicitação pendente de aprovação (Candidato: Renato Silveira)
            p_renato = pessoas_civis.get("Renato Silveira (Candidato Onboarding)")
            if p_renato:
                res_sol = await session.execute(
                    select(SolicitacaoCadastroMorador).where(
                        SolicitacaoCadastroMorador.condominio_id == condo_principal.id,
                        SolicitacaoCadastroMorador.pessoa_id == p_renato.id,
                    )
                )
                if not res_sol.scalar_one_or_none():
                    solicitacao_renato = SolicitacaoCadastroMorador(
                        id=uuid.uuid4(),
                        condominio_id=condo_principal.id,
                        unidade_id=u_301.id,
                        convite_id=convite_301.id,
                        pessoa_id=p_renato.id,
                        tipo_vinculo="INQUILINO",
                        status="ENVIADA",
                        etapa_atual="VALIDACAO_DOCUMENTAL",
                        enviada_em=datetime.now(timezone.utc) - timedelta(hours=3),
                    )
                    session.add(solicitacao_renato)
                    await session.flush()

                    # Anexo de Documentos Comprobatórios
                    session.add(
                        DocumentoCadastro(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            solicitacao_cadastro_id=solicitacao_renato.id,
                            tipo_documento="DOCUMENTO_IDENTIFICACAO_FRENTE",
                            nome_original="cnh_renato_frente.pdf",
                            chave_armazenamento="uploads/cadastros/cnh_renato_frente.pdf",
                            tipo_mime="application/pdf",
                            tamanho_bytes=245100,
                            status_validacao="PENDENTE",
                        )
                    )
                    session.add(
                        DocumentoCadastro(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            solicitacao_cadastro_id=solicitacao_renato.id,
                            tipo_documento="CONTRATO_LOCACAO",
                            nome_original="contrato_locacao_apt301.pdf",
                            chave_armazenamento="uploads/cadastros/contrato_locacao_apt301.pdf",
                            tipo_mime="application/pdf",
                            tamanho_bytes=1048576,
                            status_validacao="PENDENTE",
                        )
                    )

                    # Verificação Facial e Prova de Vida
                    session.add(
                        VerificacaoFacial(
                            id=uuid.uuid4(),
                            condominio_id=condo_principal.id,
                            pessoa_id=p_renato.id,
                            solicitacao_cadastro_id=solicitacao_renato.id,
                            provedor="INTELBRAS_FACIAL",
                            tipo_verificacao="PROVA_DE_VIDA_LIVENESS",
                            resultado="APROVADA",
                            pontuacao=0.98500,
                            prova_de_vida=True,
                            consentimento_em=datetime.now(timezone.utc) - timedelta(hours=3),
                            concluida_em=datetime.now(timezone.utc) - timedelta(hours=3),
                        )
                    )

        # 2.5 Veículos e Animais Domésticos
        veiculos_seed = [
            {"placa": "BRA2E19", "tipo": "CARRO", "marca": "Toyota", "modelo": "Corolla Cross Hybrid", "cor": "Prata", "u_key": "Bloco A - Girassol_Apt 101"},
            {"placa": "SPK4H88", "tipo": "CARRO", "marca": "Jeep", "modelo": "Compass Limited", "cor": "Preto", "u_key": "Bloco A - Girassol_Apt 102"},
            {"placa": "RIO9F21", "tipo": "MOTO", "marca": "Honda", "modelo": "CB 500X", "cor": "Vermelho", "u_key": "Bloco A - Girassol_Apt 101"},
            {"placa": "DFM7A33", "tipo": "CARRO", "marca": "BYD", "modelo": "Dolphin Plus", "cor": "Azul", "u_key": "Bloco B - Orquídea_Cobertura 501"},
            {"placa": "PRT5C12", "tipo": "CARRO", "marca": "Volkswagen", "modelo": "Nivus Highline", "cor": "Cinza Moonstone", "u_key": "Bloco C - Tulipa_Duplex 101"},
        ]

        for v_data in veiculos_seed:
            res_v = await session.execute(
                select(Veiculo).where(Veiculo.condominio_id == condo_principal.id, Veiculo.placa == v_data["placa"])
            )
            if not res_v.scalar_one_or_none():
                unid_id = unidades_map[v_data["u_key"]].id if v_data["u_key"] in unidades_map else None
                session.add(
                    Veiculo(
                        id=uuid.uuid4(),
                        condominio_id=condo_principal.id,
                        unidade_id=unid_id,
                        placa=v_data["placa"],
                        tipo=v_data["tipo"],
                        marca=v_data["marca"],
                        modelo=v_data["modelo"],
                        cor=v_data["cor"],
                        status="ATIVO",
                    )
                )

        pets_seed = [
            {"nome": "Thor", "especie": "CANINO", "raca": "Golden Retriever", "porte": "GRANDE", "vacinado": True, "u_key": "Bloco A - Girassol_Apt 101"},
            {"nome": "Mia", "especie": "FELINO", "raca": "Siamês", "porte": "PEQUENO", "vacinado": True, "u_key": "Bloco A - Girassol_Apt 102"},
            {"nome": "Pipoca", "especie": "CANINO", "raca": "Poodle Toy", "porte": "PEQUENO", "vacinado": True, "u_key": "Bloco B - Orquídea_Cobertura 501"},
            {"nome": "Luna", "especie": "CANINO", "raca": "Border Collie", "porte": "MEDIO", "vacinado": True, "u_key": "Bloco C - Tulipa_Duplex 101"},
        ]

        for pet_data in pets_seed:
            res_p = await session.execute(
                select(Pet).where(Pet.condominio_id == condo_principal.id, Pet.nome == pet_data["nome"])
            )
            if not res_p.scalar_one_or_none():
                unid_id = unidades_map[pet_data["u_key"]].id if pet_data["u_key"] in unidades_map else None
                session.add(
                    Pet(
                        id=uuid.uuid4(),
                        condominio_id=condo_principal.id,
                        unidade_id=unid_id,
                        nome=pet_data["nome"],
                        especie=pet_data["especie"],
                        raca=pet_data["raca"],
                        porte=pet_data["porte"],
                        vacinado=pet_data["vacinado"],
                        status="ATIVO",
                    )
                )

        await session.commit()
        print("Massa de dados rica (BC Condomínio + BC Identidade e Cadastro) gerada com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed())
