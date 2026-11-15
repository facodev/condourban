# Gestão de Credenciais Físicas e Dispositivos de Acesso (RFID, LPR, QR Code)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Perda constante de tags RFID, clonagem de controles remotos veiculares, demora na entrada de visitantes e dificuldade em mapear quais portas e cancelas cada pessoa tem autorização para transpor.
- **Proposta de Valor:** Centralizar o ciclo de vida de todas as credenciais de acesso (tags de proximidade, chaveiros RFID, QR Codes dinâmicos com expiração temporal e antenas LPR para reconhecimento de placas), associando-as às regras de permissão física por área e horário.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `controle_acesso` |
| **Subdomínio** | `credenciais` e `dispositivos` |
| **Fase de Entrega** | Fase 2 (Operação e Acesso) |
| **Tabelas do Banco (pt-BR)** | `dispositivo_acesso`, `credencial_acesso`, `autorizacao_acesso`, `regra_acesso_horario` |
| **Perfis com Acesso** | Porteiro, Síndico, Administradora (Morador gera QR Code) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Gerar QR Code de acesso para visitante | **Sim** | **Sim** | — | **Sim** | **Sim** |
| Cadastrar nova Tag RFID / Chaveiro | — | **Sim** | — | **Sim** | **Sim** |
| Vincular tag à unidade / morador | — | **Sim** | — | **Sim** | **Sim** |
| Bloquear tag perdida ou furtada | Solicita | **Sim** | — | **Sim** | **Sim** |
| Configurar regras de áreas e horários | — | — | — | **Sim** | **Sim** |

---

## 4. Tipos de Credenciais Suportadas

| Tipo de Credencial | Tecnologia | Aplicação Típica |
| :--- | :--- | :--- |
| `FACIAL` | Reconhecimento Facial (Template) | Portões de pedestres e acessos sociais |
| `TAG_RFID` | Proximidade Mifare 13.56MHz ou 125kHz | Chaveiros de pedestres e tags veiculares |
| `PLACA_VEICULAR` | Leitura Óptica de Placas (LPR / OCR) | Cancelas e portões de veículos |
| `QR_CODE` | QR Code Criptografado Dinâmico (TOTP) | Visitantes, convidados de festas e prestadores |
| `SENHA_NUMERICA` | Senha digitável em teclado físico | Fallback de contingência e prestadores |

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Cadastro e Associação de Tag RFID na Portaria
1. O morador comparece à guarita com um novo chaveiro de aproximação.
2. O porteiro clica em `Controle de Acesso > Vincular Nova Tag`.
3. O leitor USB de mesa da guarita captura o código hexadecimal da tag (ex: `A1B2C3D4`).
4. O porteiro busca o morador e sua respectiva unidade.
5. Seleciona o perfil de acesso (ex: "Morador - Acesso Livre a Portões e Garagem").
6. O sistema grava em `credencial_acesso` e aciona a tarefa de sincronização com as controladoras de porta correspondentes.

### 5.2 Emissão de QR Code Dinâmico para Visitante
1. O morador abre o app e clica em **"Gerar Acesso Rápido"**.
2. Define a vigência: Ex: *Válido hoje das 14h00 às 20h00, 1 única entrada*.
3. O app gera um token JWT efêmero embutido em QR Code.
4. O visitante aproxima a tela do smartphone da leitora de QR Code do totem da portaria.
5. A leitora valida a assinatura criptográfica, aciona a abertura da catraca/porta e emite o evento de passagem.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Nenhuma credencial RFID pode estar vinculada a mais de uma pessoa física simultaneamente.
- **RN-02:** O bloqueio de uma credencial (por perda, furto ou inadimplência contratual) propaga imediatamente para o hardware em menos de 10 segundos.
- **RN-03:** QR Codes temporários de visitantes expiram impreterivelmente após o prazo configurado ou após o número máximo de acessos autorizados ser atingido.
- **RN-04:** Prestadores de serviços só podem possuir regras de acesso ativas em dias úteis e horários comerciais delimitados (conforme convenção do condomínio).

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/controle-acesso/`)
- `POST /api/v1/controle-acesso/credenciais`: Cadastro de nova credencial física.
- `PATCH /api/v1/controle-acesso/credenciais/{id}/bloquear`: Bloqueio imediato de tag.
- `POST /api/v1/controle-acesso/qr-code/gerar`: Emissão de QR Code temporário assinado com HMAC.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `tag.bloqueada` | Morador titular | Push + E-mail | "A Tag de acesso final 1234 vinculada à sua unidade foi bloqueada." |
| `qr_code.utilizado` | Morador autor | Push | "Seu visitante utilizou o QR Code e acessou a Portaria Social." |
