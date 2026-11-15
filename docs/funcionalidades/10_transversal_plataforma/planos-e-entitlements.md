# Catálogo de Planos SaaS e Entitlements (Módulos Habilitáveis)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Necessidade comercial de comercializar a plataforma em diferentes planos (Starter, Essencial, Acesso Inteligente, Administradora) sem ter que manter múltiplos repositórios de código ou ramificações de software, permitindo ativar ou desligar módulos sob demanda por condomínio com segurança em tempo de execução.
- **Proposta de Valor:** Modelo robusto de licenciamento e entitlement comercial (formalizado no [ADR-011](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-011-planos-e-funcionalidades.md)), onde a API e o frontend consultam em tempo real a função canônica de resolução de direitos (`funcionalidade_habilitada`), ocultando menus no frontend e rejeitando acessos não licenciados na API com código HTTP 403 `FEATURE_DISABLED`.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `transversal` / `saas_plataforma` |
| **Subdomínio** | `entitlements` e `planos` |
| **Fase de Entrega** | Fase 4 (Comercial e Escala) |
| **Tabelas do Banco (pt-BR)** | `plano`, `funcionalidade`, `plano_funcionalidade`, `assinatura`, `condominio_funcionalidade` |
| **Função SQL Canônica** | `funcionalidade_habilitada(condominio_id, codigo_funcionalidade)` |
| **Perfis com Acesso** | Administrador da Plataforma (gerencia catálogo e overrides); Síndico (consulta) |

---

## 3. Matriz de Planos Comerciais e Recursos Licenciados

| Bounded Context / Módulo | Código do Recurso | Plano Starter (Básico) | Plano Essencial (Operação) | Plano Acesso (IoT/Facial) | Plano Enterprise (Completo) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `identidade_cadastro` | `onboarding_membros` | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** |
| `condominio` | `estrutura_condominio`| **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** |
| `comunicacao` | `comunicados_mural` | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** |
| `comunicacao` | `livro_ocorrencias` | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** | **Incluído (Núcleo)** |
| `portaria` | `encomendas_pacotes` | — | **Incluído** | **Incluído** | **Incluído** |
| `portaria` | `visitantes_prestadores`| — | **Incluído** | **Incluído** | **Incluído** |
| `reservas` | `reserva_areas_comuns` | — | **Incluído** | **Incluído** | **Incluído** |
| `controle_acesso` | `facial_intelbras_iot` | — | — | **Incluído** | **Incluído** |
| `controle_acesso` | `acionamento_remoto` | — | — | **Incluído** | **Incluído** |
| `governanca` | `assembleias_virtuais` | — | — | — | **Incluído** |
| `financeiro` | `boletos_pix_inapp` | — | Add-on | Add-on | **Incluído** |
| `manutencao` | `pmo_preventivo` | — | Add-on | Add-on | **Incluído** |

---

## 4. Algoritmo de Resolução de Direitos (Única Fonte da Verdade)

A disponibilidade efetiva de um módulo para determinado condomínio segue rigorosamente a precedência:

```text
               ┌──────────────────────────────────────────────┐
               │ O recurso possui escopo 'NUCLEO' do sistema? │
               └──────────────────────┬───────────────────────┘
                                      │
                         Sim ─────────┴───────── Não
                          │                       │
                          ▼                       ▼
                  [SEMPRE HABILITADO]     ┌────────────────────────────────────────────────────────┐
                                          │ Existe override explícito em 'condominio_funcionalidade'│
                                          │ para este condomínio (cortesia ou bloqueio operacional)? │
                                          └───────────────────────┬────────────────────────────────┘
                                                                  │
                                                     Sim ─────────┴───────── Não
                                                      │                       │
                                                      ▼                       ▼
                                              [USA VALOR DO OVERRIDE] ┌──────────────────────────────────────┐
                                              (True = On / False = Off)│ A assinatura ATIVA/TRIAL do condomínio │
                                                                      │ inclui este módulo no plano contratado?│
                                                                      └──────────────────┬───────────────────┘
                                                                                         │
                                                                            Sim ─────────┴───────── Não
                                                                             │                       │
                                                                             ▼                       ▼
                                                                     [HABILITADO NO PLANO]   [DESABILITADO (403)]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Bloqueio de Acesso na API (Enforcement)
1. O morador tenta acessar rota restrita: `POST /api/v1/controle-acesso/facial/capturar`.
2. O middleware/dependência do FastAPI `exigir_funcionalidade("facial_intelbras_iot")` intercepta a requisição.
3. Executa a query da função SQL `funcionalidade_habilitada(condominio_id, 'facial_intelbras_iot')`.
4. Se o condomínio possui plano básico sem o módulo e sem override de cortesia, a API responde imediatamente com:
```json
{
  "codigo_erro": "FEATURE_DISABLED",
  "mensagem": "O módulo de reconhecimento facial e controle de acesso não está habilitado no plano deste condomínio.",
  "modulo": "facial_intelbras_iot"
}
```
5. O status HTTP é `403 Forbidden`.

### 5.2 Liberação de Cortesia por Override
1. O departamento comercial negocia um piloto de 30 dias de leitoras faciais para um condomínio no plano Essencial.
2. O Admin da Plataforma acessa o painel de suporte e insere um registro em `condominio_funcionalidade`:
   - `condominio_id = 123`
   - `codigo_funcionalidade = 'facial_intelbras_iot'`
   - `habilitada = true`
   - `motivo = 'Piloto de 30 dias autorizado pelo comercial'`
3. A partir desse segundo, a função SQL passa a retornar `true` e todas as telas e endpoints de biometria facial são liberados imediatamente para o condomínio.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o [ADR-011](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-011-planos-e-funcionalidades.md), permissão de usuário (RBAC) e habilitação de plano (Entitlement) são conceitos ortogonais e independentes: mesmo que o usuário seja o `SINDICO`, ele não pode operar um módulo que não esteja habilitado para o seu condomínio.
- **RN-02:** Os recursos com escopo `NUCLEO` (ex: cadastro de pessoas, blocos e unidades) nunca podem ser desabilitados nem por override nem por expiração de plano, garantindo a integridade dos dados básicos do cliente.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/saas/`)
- `GET /api/v1/condominio/funcionalidades-ativas`: Retorna array de strings com todos os códigos de recursos ativos para o frontend renderizar condicionalmente os menus.
- `POST /api/v1/plataforma/condominios/{id}/overrides`: Concessão de override operacional por analista de suporte.

### Frontend Angular (PWA)
- Diretiva estrutural `*appFeature="'reservas'"`: Oculta botões e menus caso a feature não esteja no array de funcionalidades ativas retornado na inicialização da sessão.
