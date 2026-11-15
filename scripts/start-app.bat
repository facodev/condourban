@echo off
setlocal EnableDelayedExpansion
title CondoUrban - Start App (API + Front)
color 0A
echo ============================================
echo   CondoUrban ^| API + Angular
echo ============================================
echo.

set "PROJECT_DIR=%~dp0.."
cd /d "%PROJECT_DIR%"
if errorlevel 1 (
    echo [ERRO] Nao foi possivel acessar a pasta do projeto:
    echo %PROJECT_DIR%
    pause
    exit /b 1
)

set "API_DIR=%PROJECT_DIR%\backend"
set "WEB_DIR=%PROJECT_DIR%\frontend"
set "VENV_PY=%API_DIR%\.venv\Scripts\python.exe"
set "VENV_UVICORN=%API_DIR%\.venv\Scripts\uvicorn.exe"
set "API_PORT=8000"
set "WEB_PORT=4200"

if not exist "%API_DIR%\app\main.py" (
    echo [ERRO] API nao encontrada em backend
    pause
    exit /b 1
)
if not exist "%WEB_DIR%\package.json" (
    echo [ERRO] Front nao encontrado em frontend
    pause
    exit /b 1
)

echo [1/4] Parando instancias anteriores nas portas %API_PORT% e %WEB_PORT%...
call "%~dp0stop-app.bat" quiet
ping 127.0.0.1 -n 2 >nul

if not exist "%VENV_PY%" (
    echo [ERRO] venv da API nao encontrado.
    echo        Execute: cd backend ^&^& python -m venv .venv ^&^& .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
if not exist "%VENV_UVICORN%" (
    echo [ERRO] uvicorn nao instalado no venv.
    echo        Execute: cd backend ^&^& .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
if not exist "%WEB_DIR%\node_modules\@angular\core" (
    echo [ERRO] Dependencias do front ausentes.
    echo        Execute: cd frontend ^&^& npm install --strict-ssl=false
    pause
    exit /b 1
)

echo [2/4] Seed do banco ^(idempotente^)...
pushd "%API_DIR%"
"%VENV_PY%" scripts\seed.py
if errorlevel 1 (
    echo [AVISO] Seed falhou — a API ainda sera iniciada.
)
popd

echo [3/4] Iniciando API em http://0.0.0.0:%API_PORT% ...
start "CondoUrban API" /D "%API_DIR%" cmd /k ""%VENV_UVICORN%" app.main:app --reload --host 0.0.0.0 --port %API_PORT%"

echo [4/4] Iniciando Angular em http://0.0.0.0:%WEB_PORT% ...
start "CondoUrban Front" /D "%WEB_DIR%" cmd /k "npm start"

echo.
echo [OK] API:       http://localhost:%API_PORT%/docs
echo [OK] App:       http://localhost:%WEB_PORT%/
echo [OK] Admin:     admin@condourban.com / admin123
echo [OK] Sindico:   sindico@condourban.com / admin123
echo [OK] Portaria:  portaria@condourban.com / admin123
echo [OK] Encomendas:encomendas@condourban.com / admin123
echo [OK] Morador:   morador@condourban.com / admin123
echo.
echo [INFO] Duas janelas foram abertas ^(API e Front^).
echo [INFO] Para parar: scripts\stop-app.bat
echo.

start "" cmd /c "ping 127.0.0.1 -n 8 >nul && start http://127.0.0.1:%WEB_PORT%/"

pause
exit /b 0
