# Auto-cadastro de morador

## 1. Convite

O administrador cria um convite associado a:

- condomínio;
- unidade;
- tipo de vínculo;
- validade.

O convite pode ser:

- link;
- código;
- QR Code.

## 2. Identificação

O usuário informa:

- nome completo;
- nome social;
- CPF;
- data de nascimento;
- sexo, quando necessário;
- e-mail;
- celular.

## 3. Documento

Aceitar:

- RG;
- CIN;
- CNH;
- passaporte.

Podem ser exigidos frente e verso.

## 4. Comprovante de vínculo

### Proprietário
- matrícula;
- escritura;
- instrumento de aquisição;
- documento aceito pelo condomínio.

### Inquilino
- contrato de locação.

### Morador autorizado
- autorização do proprietário ou responsável.

## 5. Facial

Fluxo:

```text
Câmera
  |
  +--> captura
  |
  +--> prova de vida
  |
  +--> comparação/validação
  |
  +--> referência externa
```

A imagem e a biometria devem ter política de retenção definida.

## 6. Análise

Administrador visualiza:

- dados;
- documentos;
- comprovante;
- resultado facial;
- divergências;
- histórico.

Ações:

- aprovar;
- solicitar correção;
- rejeitar.

## 7. Aprovação

Transação lógica:

```text
Solicitação APROVADA
       |
       +--> pessoa ativa
       +--> membro do condomínio
       +--> ocupação da unidade
       +--> usuário, quando necessário
       +--> credencial facial
       +--> autorização
       +--> sincronização Intelbras
```

## 8. Correção

Motivos padronizados:

- documento ilegível;
- documento incompleto;
- documento inválido;
- dados divergentes;
- comprovante insuficiente;
- facial inconclusiva;
- prova de vida reprovada;
- outro.

## 9. Regra de segurança

O candidato não escolhe livremente a unidade.

A unidade deve ser determinada pelo convite ou por processo administrativo controlado.
