import json
from pathlib import Path
import pytest


FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / 'frontend'


def test_auth_guard_redireciona_para_login():
    guard_path = FRONTEND_DIR / 'src' / 'app' / 'core' / 'guards' / 'auth.guard.ts'
    assert guard_path.exists(), f'Arquivo auth.guard.ts não encontrado em {guard_path}'
    content = guard_path.read_text(encoding='utf-8')

    # Validações estáticas do contrato do guard
    assert 'export const authGuard: CanActivateFn' in content
    assert 'isAuthenticated()' in content
    assert "['/auth/login']" in content


def test_papel_guard_bloqueia_rota_admin():
    guard_path = FRONTEND_DIR / 'src' / 'app' / 'core' / 'guards' / 'papel.guard.ts'
    assert guard_path.exists(), f'Arquivo papel.guard.ts não encontrado em {guard_path}'
    content = guard_path.read_text(encoding='utf-8')

    assert 'export const papelGuard: CanActivateFn' in content
    assert 'hasAnyRole(papeisPermitidos)' in content
    assert "['/comunicacao']" in content


def test_encomendas_sem_mock_e_com_pin():
    ts = (
        FRONTEND_DIR
        / 'src'
        / 'app'
        / 'features'
        / 'portaria'
        / 'components'
        / 'encomendas'
        / 'encomendas.component.ts'
    )
    html = (
        FRONTEND_DIR
        / 'src'
        / 'app'
        / 'features'
        / 'portaria'
        / 'components'
        / 'encomendas'
        / 'encomendas.component.html'
    )
    assert ts.exists() and html.exists()
    ts_content = ts.read_text(encoding='utf-8')
    html_content = html.read_text(encoding='utf-8')
    assert 'getEncomendas' in ts_content
    assert 'ML-9921' not in ts_content
    assert 'AMZ-1044' not in ts_content
    assert 'codigoRetirada' in html_content


def test_menu_morador_inclui_portaria():
    app_ts = FRONTEND_DIR / 'src' / 'app' / 'app.component.ts'
    content = app_ts.read_text(encoding='utf-8')
    assert "'portaria'" in content
    # Morador branch must list portaria among allowed modules
    assert "['comunicacao', 'reservas', 'identidade', 'financeiro', 'portaria']" in content


def test_encomendas_empty_loading_error_states():
    html = (
        FRONTEND_DIR
        / 'src'
        / 'app'
        / 'features'
        / 'portaria'
        / 'components'
        / 'encomendas'
        / 'encomendas.component.html'
    )
    content = html.read_text(encoding='utf-8')
    assert 'state-empty' in content
    assert 'Nenhuma encomenda registrada' in content
    assert 'state-loading' in content
    assert 'state-error' in content
    assert 'Carregando encomendas' in content


def test_encomendas_baixa_somente_operador():
    ts = (
        FRONTEND_DIR
        / 'src'
        / 'app'
        / 'features'
        / 'portaria'
        / 'components'
        / 'encomendas'
        / 'encomendas.component.ts'
    )
    html = (
        FRONTEND_DIR
        / 'src'
        / 'app'
        / 'features'
        / 'portaria'
        / 'components'
        / 'encomendas'
        / 'encomendas.component.html'
    )
    ts_content = ts.read_text(encoding='utf-8')
    html_content = html.read_text(encoding='utf-8')
    assert 'podeOperarEncomendas' in ts_content
    assert 'podeBaixar()' in html_content
    assert 'Registrar Retirada' in html_content


def test_manifest_e_service_worker_presentes():
    manifest_path = FRONTEND_DIR / 'src' / 'manifest.webmanifest'
    assert manifest_path.exists(), f'Arquivo manifest.webmanifest não encontrado em {manifest_path}'

    manifest_data = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    assert 'name' in manifest_data

    assert 'icons' in manifest_data
    assert manifest_data.get('display') == 'standalone'

    app_config_path = FRONTEND_DIR / 'src' / 'app' / 'app.config.ts'
    assert app_config_path.exists(), f'Arquivo app.config.ts não encontrado em {app_config_path}'
    app_config_content = app_config_path.read_text(encoding='utf-8')

    assert 'provideServiceWorker' in app_config_content
    assert 'ngsw-worker.js' in app_config_content
