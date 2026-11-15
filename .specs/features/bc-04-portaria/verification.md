# Bounded Context 04: Portaria — Atendimento e Correspondências verification

**Verdict**: PASS
**Profile**: light
**Diff range**: 036938f..13d0db4 (`036938f..HEAD`)
**Round**: 1 - full
**Verifier**: independent sub-agent (author != verifier)

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | POST encomendas com ENCOMENDAS persiste RECEBIDA, PIN 4 dígitos, 201 | `pytest tests/test_portaria.py tests/test_frontend_contracts.py -k "…"` — `test_encomendas_create_list_baixa_por_encomendas` PASSED | `backend/tests/test_portaria.py:54` — `assert create_res.status_code == 201`; `:56` — `assert data['status'] == 'RECEBIDA'`; `:59` — `assert len(data['codigo_retirada']) == 4` | PASS |
| C2 | GET encomendas com ENCOMENDAS retorna lista 200 | same — PASSED | `backend/tests/test_portaria.py:64` — `assert list_res.status_code == 200`; `:66` — `assert any(item['id'] == encomenda_id for item in lista)` | PASS |
| C3 | Baixa com PIN correto → ENTREGUE, retirada_em, 200 | same — PASSED | `backend/tests/test_portaria.py:73` — `assert baixa_res.status_code == 200`; `:75` — `assert entregue['status'] == 'ENTREGUE'`; `:76` — `assert entregue['retirada_em'] is not None` | PASS |
| C4 | Baixa com PIN incorreto → 400 PIN_INVALIDO | same — `test_baixa_pin_invalido_retorna_400` PASSED | `backend/tests/test_portaria.py:114` — `assert bad.status_code == 400`; `:115` — `assert bad.json()['detail'] == 'PIN_INVALIDO'` | PASS |
| C5 | POST encomendas por MORADOR ou só PORTARIA → 403 | same — `test_post_encomenda_morador_e_portaria_retorna_403` PASSED | `backend/tests/test_portaria.py:130` — `assert res.status_code == 403, papel` (loop MORADOR/PORTARIA/PORTEIRO) | PASS |
| C6 | GET encomendas por MORADOR só da própria unidade, 200 | same — `test_morador_lista_somente_propria_unidade` PASSED | `backend/tests/test_portaria.py:166` — `assert list_res.status_code == 200`; `:168` — `assert id_a in ids` | PASS |
| C7 | Morador não vê encomenda de outra unidade | same — PASSED | `backend/tests/test_portaria.py:169` — `assert id_b not in ids` | PASS |
| C8 | UI encomendas consome API (sem mock) e expõe PIN RECEBIDA | same — `test_encomendas_sem_mock_e_com_pin` PASSED | `backend/tests/test_frontend_contracts.py:54` — `assert 'getEncomendas' in ts_content`; `:55-56` — mock IDs ausentes; `:57` — `assert 'codigoRetirada' in html_content` | PASS |
| C9 | Menu do morador inclui portaria | same — `test_menu_morador_inclui_portaria` PASSED | `backend/tests/test_frontend_contracts.py:65` — `assert "['comunicacao', 'reservas', 'identidade', 'financeiro', 'portaria']" in content` | PASS |
| C10 | Estado vazio legível na tela de encomendas | same — `test_encomendas_empty_loading_error_states` PASSED | `backend/tests/test_frontend_contracts.py:80` — `assert 'state-empty' in content`; `:81` — `assert 'Nenhuma encomenda registrada' in content` | PASS |
| C11 | POST visitantes com PORTARIA → 201 | same — `test_visitantes_portaria_cria_e_lista` PASSED | `backend/tests/test_portaria.py:188` — `assert create_res.status_code == 201`; `:190` — `assert data['id'] is not None` | PASS |
| C12 | GET visitantes com PORTARIA → 200 | same — PASSED | `backend/tests/test_portaria.py:194` — `assert list_res.status_code == 200`; `:195` — `assert any(item['id'] == data['id'] for item in list_res.json())` | PASS |
| C13 | POST visitantes por MORADOR ou só ENCOMENDAS → 403 | same — `test_post_visitante_morador_e_encomendas_retorna_403` PASSED | `backend/tests/test_portaria.py:210` — `assert res.status_code == 403, papel` | PASS |
| C14 | GET/POST encomendas e visitantes sem Bearer → 401 | same — `test_portaria_sem_token_retorna_401` PASSED | `backend/tests/test_portaria.py:231` — `assert res.status_code == 401, path` (4 rotas) | PASS |
| C15 | Suíte BC-01/BC-02 permanece verde | `pytest tests/test_identidade.py tests/test_ocupacao_unidade.py tests/test_onboarding_veiculos.py tests/test_auth.py tests/test_condominio.py` — 41 passed | BC-01 `backend/tests/test_auth.py:33` — `assert login_res.status_code == 200`; BC-02 `backend/tests/test_condominio.py:24` — `assert post_res.status_code == 201`; full named suite exit 0 | PASS |
| C16 | Critérios 1–14 cobertos por provas pytest nomeadas | `pytest tests/test_portaria.py --collect-only -q` — 7 collected; plus frontend contract defs for C8–C10 | `backend/tests/test_portaria.py:38,80,119,134,173,199,214` (API C1–C7/C11–C14); `backend/tests/test_frontend_contracts.py:30,60,68` (C8–C10) — named defs exist and ran under C1–C14 | PASS |
| C17 | Estado de erro na tela sem dados fictícios | same batch — `test_encomendas_empty_loading_error_states` PASSED | `backend/tests/test_frontend_contracts.py:83` — `assert 'state-error' in content` (mock absence co-settled by C8 `:55-56`) | PASS |
| C18 | Baixa na UI só operador; morador vê PIN sem botão baixa | same — `test_encomendas_baixa_somente_operador` PASSED | `backend/tests/test_frontend_contracts.py:110` — `assert 'podeOperarEncomendas' in ts_content`; `:111` — `assert 'podeBaixar()' in html_content`; `:112` — `assert 'Registrar Retirada' in html_content` | PASS |

## Swept existing

Re-read against code at `13d0db4` (rows that resolve to existing, not `n/a`):

| Sweep | Cited via | Present in code? |
| --- | --- | --- |
| validation | C1, C4, C11 | yes — create returns RECEBIDA+PIN (`encomendas/service.py:56,60`); PIN mismatch raises `PIN_INVALIDO` (`service.py:91-94`); visitante create gated (`atendimento/router.py:30-32`) |
| failure modes | C4, C5, C13, C14 | yes — `PIN_INVALIDO` 400; `exigir_papel` on encomendas create/baixa (`encomendas/router.py:59-62,84-87`); visitantes (`atendimento/router.py:30-32,49-51`); Bearer required (C14 test pops override) |
| authorization | C5, C6, C13, C14, C18 | yes — `PAPEIS_OPERACAO_ENCOMENDAS` / `PAPEIS_OPERACAO_VISITANTES` (`rbac.py:43-68`); list filter `unidade_id.in_(unidade_ids)` (`encomendas/service.py:29-32`); UI `podeBaixar` → `podeOperarEncomendas` |
| data lifecycle | C1, C3 | yes — create `status='RECEBIDA'`; baixa sets `ENTREGUE` + `retirada_em` (`service.py:96-97`) |
| dependency failure | C17 | yes — `state-error` banner in `encomendas.component.html:12` |
| state transitions | C3, C4 | yes — PIN gate before `ENTREGUE` (`service.py:91-96`); wrong PIN does not transition |
| idempotency / concurrency / observability | n/a | approved policy — nothing to contradict |

## Level / sampling

- API checks C1–C7, C11–C14 assert HTTP status and named response fields at the FastAPI boundary (`AsyncClient`) — matches checks.md Test policy (boundary).
- UI checks C8–C10, C17–C18 are source-contract string assertions over Angular files — matches policy (no browser harness under light).
- Sampling: one shared flow test covers C1–C3; C6/C7 share one list assertion pair; acceptable under light (single case per claim, no overclaim of unexercised statuses inside the check text).
- Note (non-blocking under light; Coverage not recomputed): checks.md Coverage table maps `422` to C1/C11 and baixa `403`/`404` to C5/C3, but those members are not asserted by the named proofs — the **check claims themselves** do not require those statuses.

## Gate

```text
.\.venv\Scripts\python.exe -m pytest tests/test_portaria.py tests/test_frontend_contracts.py -k "test_encomendas_create_list_baixa_por_encomendas or test_baixa_pin_invalido_retorna_400 or test_post_encomenda_morador_e_portaria_retorna_403 or test_morador_lista_somente_propria_unidade or test_encomendas_sem_mock_e_com_pin or test_menu_morador_inclui_portaria or test_encomendas_empty_loading_error_states or test_visitantes_portaria_cria_e_lista or test_post_visitante_morador_e_encomendas_retorna_403 or test_portaria_sem_token_retorna_401 or test_encomendas_baixa_somente_operador" -o addopts=
→ 11 passed, 3 deselected

.\.venv\Scripts\python.exe -m pytest tests/test_identidade.py tests/test_ocupacao_unidade.py tests/test_onboarding_veiculos.py tests/test_auth.py tests/test_condominio.py -o addopts=
→ 41 passed

.\.venv\Scripts\python.exe -m pytest tests/test_portaria.py --collect-only -q -o addopts=
→ 7 tests collected
```

**Gate totals**: 52 pytest cases passed across named proof runs (11 feature + 41 regression), 0 failed; collect-only listed 7 portaria API tests.
