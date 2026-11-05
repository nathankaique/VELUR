@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "VELOUR_PORT=8765"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -u CONECTAR_SUPABASE.py
) else (
  python -u CONECTAR_SUPABASE.py
)
echo.
echo Se houve erro, veja as linhas acima.
pause
