@echo off
set "QUIET="
if /i "%~1"=="quiet" set "QUIET=1"
if not defined QUIET (
    title CondoUrban - Parando App
    color 0C
    echo ============================================
    echo   CondoUrban ^| Parando API + Front
    echo ============================================
    echo.
)

set "FOUND="

call :kill_port 8000
call :kill_port 4200

if not defined FOUND (
    if not defined QUIET echo [INFO] Nenhum processo nas portas 8000/4200.
) else (
    if not defined QUIET echo [OK] Processos finalizados.
)

if defined QUIET exit /b 0
echo.
echo Concluido.
ping 127.0.0.1 -n 2 >nul
exit /b 0

:kill_port
set "PORT=%~1"
if not defined QUIET echo Procurando processos na porta %PORT%...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT% " ^| findstr LISTENING') do (
    if not defined QUIET echo [OK] Parando PID %%a na porta %PORT%...
    taskkill /PID %%a /T /F >nul 2>&1
    set "FOUND=1"
)
exit /b 0
