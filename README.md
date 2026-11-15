# App de Condomínio — CondoUrban (Web + PWA)

Fonte da verdade de produto: [`docs/`](docs/README.md).  
**Código:** API FastAPI (backend/) + Angular 22 (frontend/).

## Onde começar

| Prioridade | Documento |
|------------|-----------|
| 1 | [Status e próximos passos](docs/plano/04-status-e-proximos-passos.md) |
| 2 | [API README](backend/README.md) · [web-app README](frontend/README.md) |
| 3 | [Índice dos planos](docs/plano/INDICE.md) |
| 4 | [ADR-001 Stack Tecnológica](docs/decisoes/ADR-001-documentacao-e-stack-tecnologica.md) |
| — | **[Landing page (preview)](landing/index.html)** · [Hub de design](index.html) |

## Setup local (spike)

```bash
# Atalho Windows (API + Front)
scripts\start-app.bat
# Parar: scripts\stop-app.bat
```

Ou manualmente:

```bash
# API
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload --port 8000

# Front (outro terminal)
cd frontend
npm install
npm start
```

- API docs: http://127.0.0.1:8000/api/v1/docs  
- App: http://localhost:4200  
- Demo: `sindico@condourban.com` / `admin123` (ou `morador@condourban.com`)

| Script | Uso |
|--------|-----|
| [`scripts/start-app.bat`](scripts/start-app.bat) | API (8000) + Angular (4200) |
| [`scripts/stop-app.bat`](scripts/stop-app.bat) | Encerra portas 8000 e 4200 |
| [`scripts/start-local.bat`](scripts/start-local.bat) | Preview HTML design (8016) |

```bash
cp .env.example .env
# edite .env — nunca commite este arquivo
```

## Atualizar ao trabalhar

1. `docs/historico/CHANGELOG.md`
2. Journal opcional em `docs/historico/journal/`
3. ADR em `docs/decisoes/` se for decisão importante
4. Planos em `docs/plano/` se mudar escopo/fase
