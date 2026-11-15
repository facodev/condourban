@echo off
setlocal EnableDelayedExpansion
title Gestao Condominios - Cloudflare Tunnel (Porta 8016)
color 0A

echo ============================================
echo   Gestao Condominios ^| Tunnel Cloudflare
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
    echo        Verifique sincronizacao do OneDrive.
    pause
    exit /b 1
)

set "PORT=8016"

where cloudflared >nul 2>&1
if errorlevel 1 (
    echo [ERRO] cloudflared nao encontrado no PATH.
    echo Instale via: winget install Cloudflare.cloudflared
    pause
    exit /b 1
)

call :resolver_python
if errorlevel 1 (
    pause
    exit /b 1
)

echo [1/3] STOP - Parando instancias anteriores...
call "%~dp0stop.bat" quiet
taskkill /IM cloudflared.exe /F >nul 2>&1
ping 127.0.0.1 -n 2 >nul

echo [2/3] START - Iniciando servidor estatico na porta %PORT%...
rem Inicia o http.server em processo separado (nao depende de run-server-bg.bat)
if /i "%PY%"=="py -3" (
    powershell -NoProfile -Command "Start-Process -FilePath 'py' -ArgumentList '-3','-m','http.server','%PORT%','--bind','127.0.0.1' -WorkingDirectory '%PROJECT_DIR%' -WindowStyle Minimized"
) else (
    powershell -NoProfile -Command "Start-Process -FilePath '%PY%' -ArgumentList '-m','http.server','%PORT%','--bind','127.0.0.1' -WorkingDirectory '%PROJECT_DIR%' -WindowStyle Minimized"
)

echo Aguardando servidor na porta %PORT%...
call :aguardar_porta %PORT% 40
if errorlevel 1 (
    echo [ERRO] Servidor nao iniciou na porta %PORT%.
    echo        Na pasta do projeto, teste: python -m http.server %PORT% --bind 127.0.0.1
    pause
    exit /b 1
)
echo [OK] Servidor ativo em http://127.0.0.1:%PORT%

echo.
echo [3/3] CLOUDFLARE - Iniciando tunel para http://127.0.0.1:%PORT%
echo [INFO] Fluxo: stop -> start -> tunnel (uma unica janela).
echo [INFO] Mantenha esta janela aberta enquanto usar o tunel.
echo [INFO] Se a URL abrir com erro, confirme que apareceu "[OK] Servidor ativo" acima.
echo.
set "TUNNEL_ERR=1"
for /l %%i in (1,1,3) do (
    if %%i gtr 1 (
        echo.
        echo Tentativa %%i de 3...
        ping 127.0.0.1 -n 3 >nul
    )
    cloudflared tunnel --url http://127.0.0.1:%PORT%
    set "TUNNEL_ERR=!ERRORLEVEL!"
    if "!TUNNEL_ERR!"=="0" goto tunnel_fim
)
:tunnel_fim

call :cleanup

if not "!TUNNEL_ERR!"=="0" (
    echo.
    echo [ERRO] O tunnel encerrou com codigo !TUNNEL_ERR!.
    echo        O servidor local pode estar OK em http://127.0.0.1:%PORT%
    pause
)
exit /b !TUNNEL_ERR!

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

:porta_em_uso
powershell -NoProfile -Command "$c = New-Object System.Net.Sockets.TcpClient; try { $c.Connect('127.0.0.1', %1); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
exit /b %errorlevel%

:aguardar_porta
set "AP_PORT=%~1"
set "AP_MAX=%~2"
set /a AP_N=0
:aguardar_loop
call :porta_em_uso %AP_PORT%
if !errorlevel! equ 0 exit /b 0
set /a AP_N+=1
if !AP_N! geq %AP_MAX% exit /b 1
ping 127.0.0.1 -n 2 >nul
goto aguardar_loop

:cleanup
echo.
echo [INFO] Encerrando servidor iniciado pelo tunel...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT% " ^| findstr LISTENING') do (
    taskkill /PID %%a /T /F >nul 2>&1
)
exit /b 0
