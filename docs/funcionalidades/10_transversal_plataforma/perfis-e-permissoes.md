# Matriz de Perfis, Permissões e Controle de Acesso Baseado em Papéis (RBAC)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Vazamento de dados sigilosos (como faturas ou multas de vizinhos), porteiros com permissão indevida para alterar cadastros civis, ou síndicos sem ferramentas para delegar funções operacionais específicas ao zelador ou subsíndico com rastreabilidade.
- **Proposta de Valor:** Estabelecer a matriz canônica de Controle de Acesso Baseado em Papéis (Role-Based Access Control — RBAC) integrada à segurança de dados multi-tenant por Row-Level Security (RLS) no PostgreSQL, garantindo o princípio do menor privilégio (least privilege) em todos os endpoints e telas do sistema.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `transversal` / `identidade_cadastro` |
| **Subdomínio** | `seguranca` e `autorizacao` |
| **Fase de Entrega** | Transversal a todas as Fases |
| **Tabelas do Banco (pt-BR)** | `membro_condominio`, `papel_usuario`, `permissao_papel`, `ocupacao_unidade` |
| **Guards no Frontend** | `papel.guard.ts` e `condominio.guard.ts` |

---

## 3. Catálogo Canônico de Papéis (Roles)

| Papel (Código) | Nome de Exibição | Escopo Típico | Responsabilidade Primária |
| :--- | :--- | :--- | :--- |
| `MORADOR_TITULAR` | Morador Titular | Unidade Autônoma | Proprietário ou inquilino responsável; acesso pleno às reservas, autorizações e finanças da unidade. |
| `DEPENDENTE` | Dependente | Unidade Autônoma | Familiar residente; pode abrir chamados, gerar convites e consultar mural (finanças restritas por padrão). |
| `PORTEIRO` | Operador de Portaria | Guarita / Acessos | Liberação de entrada na guarita, conferência de visitantes/prestadores e visualização de alertas de pânico. **Não** opera recebimento/baixa de correspondências. |
| `PORTARIA` | Alias operacional de `PORTEIRO` | Guarita / Acessos | Mesmo escopo de liberação de entrada; usado no seed e JWT (`tipo_pessoa=PORTARIA`). |
| `ENCOMENDAS` | Operador de Encomendas / Correspondências | Guarita / Pacotes | Recebimento com foto, custódia e baixa de encomendas com PIN. **Não** libera entrada de visitantes. |
| `ZELADOR` | Zelador / Manutenção | Condomínio | Gestão de ordens de serviço, execução de vistorias de reservas, checklists de manutenção preventiva e, quando designado, apoio à baixa de encomendas. |
| `SINDICO` | Síndico / Gestor | Condomínio | Gestão integral do condomínio, aprovação de cadastros, comunicados oficiais, assembleias e deliberações. |
| `CONSELHO_FISCAL` | Conselheiro Fiscal | Condomínio | Acesso a pastas contábeis, relatórios de prestação de contas, despesas e emissão de pareceres mensais. |
| `ADMINISTRADORA` | Administradora | Multi-Condomínio | Gestão de faturamento, conciliação contábil, suporte operacional e auditoria para múltiplos tenants. |
| `ADMIN_PLATAFORMA` | Administrador Global | Plataforma (Superuser) | Operação da infraestrutura, catálogo comercial SaaS, auditoria global e suporte técnico com impersonation. |

---

## 4. Matriz de Permissões por Bounded Context

| Bounded Context | Morador | Dependente | Porteiro | Encomendas | Zelador | Síndico | Conselho | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `identidade_cadastro` | Próprio | Próprio | Leitura portaria | Leitura unidades | Leitura básica | Total (Condo) | Leitura | Total (Condo) |
| `condominio` | Leitura | Leitura | Leitura | Leitura | Leitura | Total (Condo) | Leitura | Total (Condo) |
| `controle_acesso` | Próprio / Convite | Próprio | Operação guarita | — | Leitura | Total (Condo) | — | Total (Condo) |
| `portaria` | Próprio (encomenda/visita) | Próprio | Visitantes (entrada) | Encomendas (create/baixa) | Apoio encomendas | Total (Condo) | — | Total (Condo) |
| `reservas` | Solicitar / Convidado | Convidado | Leitura dia | — | Vistorias | Total (Condo) | — | Total (Condo) |
| `comunicacao` | Criar ocorrência / Ler | Criar ocorrência / Ler | Ocorrência portaria | — | OS / Ocorrência | Total (Condo) | Leitura | Total (Condo) |
| `governanca` | Votar (adimplente) | Ouvinte | — | — | — | Total (Condo) | Total (Pasta) | Total (Condo) |
| `financeiro` | Faturas da unidade | — | — | — | — | Total (Condo) | Total (Contas) | Total (Faturamento) |
| `manutencao` | Abrir chamado | Abrir chamado | Reportar | — | Executar OS | Total (Condo) | — | Total (Condo) |

---

## 5. Regras de Segurança e Invariantes

- **RN-01:** O `condominio_id` e os papéis atribuídos ao usuário são assinados no payload do token JWT no login; qualquer requisição que tente acessar dados de outro condomínio é barrada tanto pelo middleware quanto pelas políticas de Row-Level Security (RLS) no PostgreSQL.
- **RN-02:** Um usuário com perfil de `MORADOR` nunca tem permissão para acessar endpoints de listagem de inadimplência geral ou dados de pagamento de outras unidades.
- **RN-03:** Ações executadas sob o papel de `ADMIN_PLATAFORMA` operando em nome de um cliente (impersonation auditado) exigem justificativa obrigatória e geram alerta para o síndico do condomínio acessado.

---

## 6. Integração Técnica com Frontend Angular

- O guard `papel.guard.ts` intercepta a navegação no Angular PWA:
```typescript
canActivate(route: ActivatedRouteSnapshot): boolean {
  const papeisPermitidos = route.data['papeis'] as string[];
  return this.authService.temPapel(papeisPermitidos);
}
```
- Rotas são configuradas com carregamento lazy e validação de perfil estrita:
```typescript
{
  path: 'portaria',
  loadChildren: () => import('./features/portaria/portaria.routes'),
  canActivate: [papelGuard],
  data: { papeis: ['PORTEIRO', 'PORTARIA', 'ENCOMENDAS', 'SINDICO', 'ADMINISTRADORA'] }
}
```
- Rotas de encomendas e de atendimento devem ser guardadas **separadamente** (`ENCOMENDAS` vs `PORTEIRO`/`PORTARIA`); um único `loadChildren` de `portaria` pode expor ambos, mas cada child route aplica o subconjunto correto.
