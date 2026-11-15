@echo off
setlocal EnableDelayedExpansion
title Gestao Condominios - Preview Design (Porta 8016)
color 0A
echo ============================================
echo   Gestao Condominios ^| Preview HTML
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
if not exist "index.html" (
    echo [ERRO] index.html nao encontrado na raiz do projeto.
    pause
    exit /b 1
)
set "PORT=8016"
echo [1/2] Parando instancia anterior...
call "%~dp0stop.bat" quiet
ping 127.0.0.1 -n 2 >nul
call :resolver_python
if errorlevel 1 (
    pause
    exit /b 1
)
echo [2/2] Iniciando servidor estatico...
echo [OK] Hub:     http://127.0.0.1:%PORT%/
echo [OK] Landing: http://127.0.0.1:%PORT%/landing/
echo [INFO] Mantenha esta janela aberta enquanto usar o preview.
echo.
start "" cmd /c "ping 127.0.0.1 -n 3 >nul && start http://127.0.0.1:%PORT%/"
if /i "%PY%"=="py -3" (
    py -3 -m http.server %PORT% --bind 127.0.0.1
) else (
    "%PY%" -m http.server %PORT% --bind 127.0.0.1
)
echo.
echo [INFO] Servidor encerrado.
pause
exit /b 0
:resolver_python
set "PY="
if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" set "PY=%PROJECT_DIR%\.venv\Scripts\python.exe"
if not defined PY (
    for /f "delims=" %%P in ('where python 2^>nul') do (
        if not defined PY (
            "%%P" -c "import sys" >nul 2>&1
            if not errorlevel 1 set "PY=%%P"
        )
    )
)
if not defined PY (
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3 -c "import sys" >nul 2>&1
        if not errorlevel 1 set "PY=py -3"
    )
)
if not defined PY (
    echo [ERRO] Python nao encontrado ou nao funcional.
    exit /b 1
)
echo [OK] Python: %PY%
exit /b 0
