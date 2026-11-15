# Configuração Institucional e Personalização do Condomínio

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Condomínios e administradoras exigem identidade visual personalizada no aplicativo (logotipo próprio, paleta de cores institucional) e possuem regras de convivência e horários operacionais específicos (horário de silêncio, tolerância de portaria, regras de mudança).
- **Proposta de Valor:** Permitir a personalização leve (branding tenant) e a configuração granular de parâmetros operacionais do condomínio sem necessidade de alterações no código-fonte, respeitando a separação entre identidade visual e catálogo de planos comerciais.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `condominio` |
| **Subdomínio** | `estrutura` / `configuracoes` |
| **Fase de Entrega** | Fase 1 (Fundação JSONB) / Fase 4 (UX Completa de Personalização) |
| **Tabelas do Banco (pt-BR)** | `condominio` (coluna `configuracoes` JSONB) |
| **Perfis com Acesso** | Síndico, Administradora, Admin da Plataforma |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora | Admin Plataforma |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Visualizar branding e regras do condomínio | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** |
| Alterar logotipo e cor primária do condomínio | — | — | — | **Sim** | **Sim** | **Sim** |
| Configurar horários de silêncio e mudança | — | — | — | **Sim** | **Sim** | **Sim** |
| Definir tolerância de cancelamento de reservas | — | — | — | **Sim** | **Sim** | **Sim** |

---

## 4. Estrutura do Schema de Configuração (`configuracoes` JSONB)

```json
{
  "branding": {
    "nome_fantasia": "Residencial Jardins do Parque",
    "logo_url": "https://s3.condourban.app/condominios/123/logo.png",
    "cor_primaria": "#1E3A8A",
    "cor_secundaria": "#3B82F6"
  },
  "regras_operacionais": {
    "horario_silencio_inicio": "22:00",
    "horario_silencio_fim": "08:00",
    "tolerancia_atraso_visitante_minutos": 15,
    "permitir_mudanca_sabado": true,
    "permitir_mudanca_domingo": false,
    "horario_mudanca_inicio": "08:00",
    "horario_mudanca_fim": "17:00"
  },
  "contato_administracao": {
    "telefone_portaria": "(11) 3456-7890",
    "email_sindico": "sindico@jardinsdoparque.com.br",
    "whatsapp_atendimento": "(11) 98765-4321"
  }
}
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Atualização de Logotipo e Cores pelo Síndico
1. O síndico acessa `Administração > Configurações do Condomínio > Personalização`.
2. Faz o upload da imagem do logotipo institucional (formato PNG ou SVG, fundo transparente).
3. Seleciona a cor de destaque (hexadecimal) através de um seletor de cores acessível.
4. O app exibe pré-visualização instantânea do cabeçalho e da tela de login.
5. Ao clicar em **"Salvar Configurações"**, a API valida o payload JSONB contra o schema Pydantic e atualiza `condominio.configuracoes`.
6. O frontend Angular atualiza os design tokens em tempo real via CSS Variables.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Conforme o [ADR-011](file:///c:/Users/frede/Projetos%20pessoais/gestao_condominios/docs/decisoes/ADR-011-planos-e-funcionalidades.md), a coluna `configuracoes` armazena estritamente branding e parâmetros operacionais; **ativação/desativação de módulos de produto nunca reside no JSONB** (gerenciada nas tabelas de planos e entitlements).
- **RN-02:** A imagem do logotipo possui tamanho máximo de 2MB e resolução recomendada de 512x512 pixels.
- **RN-03:** A cor primária deve atender ao critério mínimo de contraste WCAG AA (mínimo 4.5:1 contra fundos claros).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/condominio/`)
- `GET /api/v1/condominio/configuracoes`: Retorna os dados públicos de branding e regras do condomínio autenticado.
- `PATCH /api/v1/condominio/configuracoes`: Atualização parcial dos parâmetros (exige papel de `SINDICO` ou `ADMINISTRADORA`).
- `POST /api/v1/condominio/configuracoes/logo`: Upload direto do logotipo para o bucket S3.

### Frontend Angular (PWA)
- Componente: `features/condominio/components/configuracao-condominio`.
- Service: Injeta dinamicamente as variáveis de estilo `--primary-color` no elemento `:root`.
