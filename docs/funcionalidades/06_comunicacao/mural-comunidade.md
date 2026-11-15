# Mural da Comunidade e Classificados Internos

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Grupos externos de WhatsApp de condomínio tornam-se caóticos, com anúncios excessivos, discussões acaloradas e golpes, enquanto moradores não encontram formas seguras de doar móveis, vender itens usados ou indicar prestadores de confiança (eletricista, diarista) para a vizinhança.
- **Proposta de Valor:** Espaço social moderado e exclusivo para a comunidade do condomínio, permitindo publicação de classificados (compra, venda e doação), indicações de serviços e caronas entre moradores, com mediação transparente e sem spam.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `comunicacao` |
| **Subdomínio** | `comunidade` e `classificados` |
| **Fase de Entrega** | Fase 4 (Comunidade / Expansão) |
| **Tabelas do Banco (pt-BR)** | `anuncio_comunidade`, `comentario_anuncio`, `denuncia_conteudo` |
| **Perfis com Acesso** | Moradores ativos (publicam e interagem); Síndico (moderação) |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Dependente | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Publicar anúncio / classificado com fotos | **Sim** | **Sim** | — | — | **Sim** | — |
| Editar ou excluir próprio anúncio | **Sim** | **Sim** | — | — | — | — |
| Denunciar publicação imprópria | **Sim** | **Sim** | — | — | — | — |
| Remover anúncio inadequado (moderação) | — | — | — | — | **Sim** | **Sim** |
| Contatar anunciante via chat seguro / WhatsApp | **Sim** | **Sim** | — | — | — | — |

---

## 4. Máquina de Estados do Anúncio

```text
[ATIVO] ──(marcado como vendido / doado)──► [FINALIZADO]
   │
   ├──(denúncia acolhida pelo síndico)──► [REMOVIDO_MODERACAO]
   │
   └──(expiração de 30 dias)──► [EXPIRADO]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Publicação de Classificado pelo Morador
1. O morador entra em `Comunidade > Classificados > Novo Anúncio`.
2. Informa:
   - **Categoria:** Móveis, Eletrônicos, Infantil, Doação, Indicação de Serviços.
   - **Título e Preço:** Ex: *"Bicicleta Infantil Aro 16 — R$ 250,00"*.
   - **Descrição e Fotos:** Até 5 fotos do item.
   - **Contato:** Permite exibir telefone ou botão direto para WhatsApp.
3. O anúncio é publicado imediatamente e visível apenas para os vizinhos do mesmo condomínio.

### 5.2 Moderação de Conteúdo
1. Se um morador publicar algo ofensivo ou comercial proibido, qualquer vizinho clica em **"Denunciar"**.
2. A gestão recebe notificação; o síndico avalia e pode ocultar a publicação com um clique.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** Anúncios expiram automaticamente após 30 dias se não forem renovados pelo autor.
- **RN-02:** A plataforma não intermedeia pagamentos nem se responsabiliza pelas transações comerciais entre vizinhos (caráter de mural comunitário gratuito).
- **RN-03:** É expressamente vedada a venda de substâncias ilícitas, armas ou produtos inflamáveis.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/comunicacao/comunidade`)
- `GET /api/v1/comunicacao/comunidade/anuncios`: Feed de classificados.
- `POST /api/v1/comunicacao/comunidade/anuncios`: Criação de anúncio com fotos no S3.
- `POST /api/v1/comunicacao/comunidade/anuncios/{id}/denunciar`: Envio de denúncia à moderação.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `anuncio.denunciado` | Síndico | Alerta In-app | "O anúncio #48 recebeu denúncias e aguarda moderação da gestão." |
