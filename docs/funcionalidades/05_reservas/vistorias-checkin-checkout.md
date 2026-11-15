# Vistorias de Áreas Comuns (Check-in e Check-out com Fotos)

## 1. Objetivo e Problema de Negócio

- **Problema de Negócio:** Litígios entre moradores e condomínio por móveis danificados, louças quebradas ou churrasqueiras entregues sujas após eventos, onde a gestão não possui provas fotográficas prévias do estado em que o salão foi entregue e devolvido.
- **Proposta de Valor:** Formalizar o processo de vistoria prévia (check-in) e posterior (check-out) através do aplicativo mobile/PWA com checklist digital de itens patrimoniais (mesas, cadeiras, geladeira, ar-condicionado), fotos comprobatórias obrigatórias e termo de entrega assinado.

---

## 2. Metadados Arquiteturais

| Atributo | Definição |
| :--- | :--- |
| **Bounded Context** | `reservas` |
| **Subdomínio** | `agendamentos` e `vistorias` |
| **Fase de Entrega** | Fase 2 (Operação) |
| **Tabelas do Banco (pt-BR)** | `vistoria_reserva`, `item_vistoria`, `reserva_area_comum` |
| **Perfis com Acesso** | Zelador / Porteiro (realiza vistoria), Morador (assina/contesta), Síndico |

---

## 3. Matriz de Ações por Perfil (RBAC)

| Ação no Sistema | Morador | Porteiro | Zelador | Síndico | Administradora |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Executar checklist de vistoria prévia (check-in) | Acompanha | **Sim** | **Sim** | **Sim** | — |
| Executar vistoria de encerramento (check-out) | Acompanha | **Sim** | **Sim** | **Sim** | — |
| Fotografar avarias ou itens quebrados | **Sim** | **Sim** | **Sim** | **Sim** | — |
| Assinar termo de vistoria na tela do app | **Sim** | **Sim** | **Sim** | **Sim** | — |
| Aprovar liberação ou retenção de caução | — | — | — | **Sim** | **Sim** |

---

## 4. Máquina de Estados da Vistoria

```text
[CHECKIN_PENDENTE] ──(vistoria inicial aprovada)──► [EM_USO] ──(fim do evento)──► [CHECKOUT_PENDENTE]
                                                                                        │
                                                                                        ├──(sem avarias)──► [APROVADA_SEM_DANOS]
                                                                                        │
                                                                                        └──(avaria registrada)──► [COM_AVARIA]
```

---

## 5. Fluxos Operacionais Passo a Passo

### 5.1 Vistoria Prévia (Check-in)
1. Antes do início da festa, o zelador e o morador comparecem ao espaço comum.
2. O zelador abre no app `Vistorias > Iniciar Vistoria Prévia`.
3. Preenche o checklist padronizado:
   - Limpeza geral do piso e bancadas: `OK`
   - Funcionamento do ar-condicionado: `OK`
   - Quantidade de mesas (10) e cadeiras (40): `OK`
   - Vidros e janelas íntegros: `OK`
4. Se houver alguma marca pré-existente (ex: risco na parede), tira foto de ressalva.
5. Morador e zelador assinam na tela do tablet/smartphone e a chave/acesso é liberado.

### 5.2 Vistoria Posterior (Check-out) e Cobrança de Avaria
1. Na manhã seguinte ao evento, o zelador inspeciona o salão.
2. Identifica que um encosto de cadeira foi quebrado.
3. O zelador fotografa a cadeira quebrada, seleciona o item no checklist e marca `IRREGULARIDADE DETECTADA`.
4. O sistema gera automaticamente um laudo com fotos, horário e assinatura digital, encaminhando para o síndico.
5. O síndico aciona a retenção da caução ou lança a taxa de ressarcimento na cota condominial da respectiva unidade.

---

## 6. Regras de Negócio Estritas (Invariantes)

- **RN-01:** O registro de qualquer avaria exige obrigatoriamente a anexação de pelo menos 1 fotografia com carimbo de data e hora (timestamp) emitido pelo servidor.
- **RN-02:** A vistoria de saída (check-out) deve ser concluída em até 12 horas úteis após o encerramento do evento para evitar alegações de danos causados por terceiros.
- **RN-03:** A liberação da caução bancária para a unidade é condicionada ao status `APROVADA_SEM_DANOS`.

---

## 7. Integração Técnica (Backend & Frontend)

### Endpoints da API FastAPI (`/api/v1/reservas/{id}/vistorias`)
- `POST /api/v1/reservas/{id}/vistorias/check-in`: Registro da vistoria inicial.
- `POST /api/v1/reservas/{id}/vistorias/check-out`: Registro da vistoria final com upload de fotos de danos.
- `GET /api/v1/reservas/{id}/vistorias`: Consulta do laudo fotográfico.

---

## 8. Notificações e Mensageria

| Evento de Disparo | Destinatário | Canal | Conteúdo da Mensagem |
| :--- | :--- | :--- | :--- |
| `vistoria.concluida_ok` | Morador titular | Push + E-mail | "Vistoria do Salão de Festas concluída com sucesso! Nenhuma irregularidade encontrada." |
| `vistoria.com_avaria` | Morador titular e Síndico | Push Urgente + E-mail | "Vistoria concluída com apontamento de avaria. Consulte as fotos e laudo no app." |
