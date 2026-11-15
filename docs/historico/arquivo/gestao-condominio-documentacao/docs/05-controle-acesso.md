# Controle de acesso e Intelbras

## 1. Objetivo

Utilizar a identidade facial cadastrada para controlar o acesso de:

- moradores;
- visitantes;
- prestadores;
- funcionários;
- demais pessoas autorizadas.

## 2. Modelo

```text
Pessoa
  |
  +--> Credencial de acesso
           |
           +--> FACIAL
           |
           +--> referência externa
           |
           +--> provedor

Pessoa
  |
  +--> Autorização
           |
           +--> período
           +--> dias
           +--> horário
           +--> unidade
           +--> regras

Dispositivo
  |
  +--> Portaria
  +--> Garagem
  +--> Área comum
```

## 3. Intelbras

A primeira implementação deve utilizar um adaptador:

```text
dominio.controle_acesso
        |
        v
ProvedorControleAcesso
        |
        v
infraestrutura.intelbras
```

O domínio não deve conhecer:

- endpoint proprietário;
- payload proprietário;
- token da Intelbras;
- modelo específico de equipamento.

## 4. Sincronização

Cada operação relevante gera uma tarefa:

```text
PENDENTE
   |
   v
PROCESSANDO
   |
   +--> CONCLUIDA
   |
   +--> FALHA -> nova tentativa
```

Deve existir:

- limite de tentativas;
- backoff;
- registro da resposta;
- correlação;
- idempotência.

## 5. Revogação

Quando o morador perde o vínculo:

```text
Ocupação encerrada
       |
       v
Autorização encerrada
       |
       v
Credencial revogada
       |
       v
Intelbras sincronizada
```

## 6. Visitante

```text
Convite criado
      |
      v
Visitante realiza cadastro
      |
      v
Facial validada
      |
      v
Autorização temporária
      |
      v
Intelbras
      |
      v
Entrada
      |
      v
Saída
      |
      v
Autorização encerrada
```

## 7. Eventos

Registrar:

- reconhecimento;
- entrada;
- saída;
- acesso autorizado;
- acesso negado;
- falha;
- dispositivo indisponível.

## 8. Reconciliação

Periodicamente, o sistema deve comparar o estado esperado com o estado retornado pelo provedor para detectar:

- credencial faltante;
- autorização divergente;
- equipamento offline;
- cadastro externo removido.

## 9. Segurança

Credenciais da Intelbras:

- nunca no código;
- nunca no Git;
- nunca em log;
- armazenadas em segredo;
- rotacionáveis.
