# Repositório Digital de Documentos do Condomínio

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Moradores e corretores solicitando constantemente cópias de convenção, regimento interno ou apólices de seguro, perda de contratos de manutenção predial e falta de arquivo histórico seguro das atas de assembleia registradas em cartório.
- **Proposta de Valor:** Biblioteca digital organizada por pastas temáticas, com controle de versão, busca textual e controle granular de permissões (documentos públicos do condomínio vs contratos restritos à diretoria/conselho fiscal).

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `governanca` |
| **Subdomínio** | `documentos` e `auditoria` |
| **Fase de Entrega** | Fase 1 (Fundação) |
| **Tabelas do Banco (pt-BR)** | `documento_condominio`, `categoria_documento`, `versao_documento` |
| **Perfis com Acesso** | Todos os moradores (leitura de documentos públicos), Síndico e Conselho (gestão) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Consultar Regimento Interno e Convenção | **Sim** | **Sim** | **Sim** | **Sim** | **Sim** |
| Baixar Atas de Assembleia registradas | **Sim** | — | — | **Sim** | **Sim** |
| Consultar Contratos com prestadores de serviço | Se público | — | — | **Sim** | **Sim** |
| Fazer upload de novos documentos (.PDF) | — | — | — | **Sim** | **Sim** |
| Definir nível de sigilo da pasta / arquivo | — | — | — | **Sim** | **Sim** |

---

## 4. Categorias Estruturais de Documentos

1. **Institucionais e Normativos:** Convenção de Condomínio, Regimento Interno, Manual do Proprietário.
2. **Governança e Assembleias:** Editais de convocação, Atas registradas em cartório, Pareceres do Conselho Fiscal.
3. **Segurança e Conformidade:** Auto de Vistoria do Corpo de Bombeiros (AVCB), Apólice de Seguro Predial, Laudo de Para-raios (SPDA), Relatório de Potabilidade da Água.
4. **Contratos e Operação:** Contrato de manutenção de elevadores, portaria remota, gerador e bombas.

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Consulta pelo Morador
1. O morador entra em `Menu > Documentos do Condomínio`.
2. Navega pelas pastas ou digita na barra de busca (ex: *"Regimento"* ou *"Seguro"*).
3. O app exibe o PDF com leitor integrado de alta velocidade e botão para download.

### 5.2 Upload de Nova Versão pelo Síndico
1. O síndico acessa `Governança > Documentos > Adicionar Documento`.
2. Seleciona a categoria, informa título, data de vigência e anexa o arquivo PDF.
3. Define se o documento é `PUBLICO` (todos os moradores) ou `RESTRITO_GESTAO` (apenas síndico, conselho e administradora).
4. O arquivo é armazenado com criptografia no bucket S3 e disponibilizado imediatamente.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Documentos públicos do condomínio não podem conter dados pessoais excessivos de moradores sem anonimização (em estrita observância à LGPD).
- **RN-02:** Documentos obrigatórios de segurança (AVCB e Apólice de Seguro) exigem cadastro da data de vencimento, disparando alertas automáticos à gestão 60 e 30 dias antes da expiração.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/governanca/documentos`)
- `GET /api/v1/governanca/documentos`: Listagem hierárquica por pastas.
- `POST /api/v1/governanca/documentos`: Upload com metadados para o S3.
- `GET /api/v1/governanca/documentos/{id}/download`: Geração de pre-signed URL temporária de download.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `documento.avcb_vencendo` | Síndico e Zelador | Alerta Urgente + E-mail | "ALERTA: O AVCB do condomínio vencerá em 30 dias. Inicie a renovação." |
