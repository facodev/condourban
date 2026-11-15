# Arquitetura

## 1. Visão geral

```text
Internet
   |
CDN / WAF / TLS
   |
Angular 22 PWA
   |
FastAPI
   |
   +-- Keycloak
   +-- PostgreSQL
   +-- Redis
   +-- Armazenamento de objetos
   +-- Trabalhadores assíncronos
   |
   +-- Provedor de controle de acesso
           |
           +-- Intelbras
```

## 2. Domínios

### Identidade e cadastro
- Pessoa
- Usuário
- Membro do condomínio
- Ocupação da unidade
- Solicitação de cadastro
- Documentos
- Verificação facial

### Condomínio
- Condomínio
- Bloco
- Unidade
- Vaga de garagem
- Área comum

### Controle de acesso
- Provedor
- Dispositivo
- Credencial
- Autorização
- Evento de acesso
- Sincronização

### Portaria
- Visitante
- Convite de visitante
- Prestador
- Encomenda

### Comunicação
- Comunicado
- Conversa
- Mensagem
- Ocorrência
- Enquete

### Administração
- Cobrança condominial
- Assembleia
- Auditoria
- Permissões

## 3. Identidade

```text
Keycloak User
      |
      v
Usuario
      |
      v
Pessoa
      |
      +--> MembroCondominio
      |
      +--> OcupacaoUnidade
```

Uma pessoa não precisa ser moradora para possuir uma identidade no sistema.

## 4. Controle de acesso

```text
Pessoa
  |
  v
CredencialAcesso
  |
  v
AutorizacaoAcesso
  |
  v
DispositivoAcesso
  |
  v
Provedor
  |
  v
Intelbras
```

A mesma infraestrutura atende moradores, visitantes e prestadores.

## 5. Eventos

Eventos de domínio devem ser publicados de forma assíncrona:

```text
CadastroAprovado
PessoaAtivada
CredencialCriada
AutorizacaoCriada
CredencialSincronizada
AcessoAutorizado
AcessoNegado
EncomendaRecebida
ReservaCriada
```

## 6. Multitenancy

O condomínio é o limite de isolamento dos dados operacionais.

A API determina o condomínio a partir da identidade autenticada e da associação autorizada. O `condominio_id` enviado pelo cliente nunca é suficiente para autorização.

O FastAPI estabelece, dentro da transação:

```sql
SET LOCAL app.condominio_id = '...';
```

O PostgreSQL aplica RLS.

## 7. Arquivos

Documentos, fotos e demais arquivos ficam em armazenamento de objetos:

```text
condominio/{condominio_id}/
  cadastros/{solicitacao_id}/
  documentos/{documento_id}/
  pessoas/{pessoa_id}/
  ocorrencias/{ocorrencia_id}/
```

O banco guarda somente metadados e a chave do objeto.

## 8. Biometria

A plataforma não deve depender do formato proprietário da biometria da Intelbras.

O domínio guarda:

- referência da pessoa;
- referência externa no provedor;
- situação da credencial;
- situação da autorização;
- resultado da verificação;
- metadados mínimos necessários.

O template biométrico bruto não deve ser armazenado no PostgreSQL salvo necessidade técnica comprovada e com controles específicos.
