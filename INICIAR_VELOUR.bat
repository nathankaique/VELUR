@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not defined VELOUR_PORT set "VELOUR_PORT=8765"
echo ==========================================
echo   VELOUR 3.2 - INICIAR SERVIDOR
echo ==========================================
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -u server.py
) else (
  python -u server.py
)
echo.
echo O servidor encerrou. Se aparecer erro, copie a ultima linha.
pause
