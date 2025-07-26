@echo off
REM Script para iniciar o ambiente de desenvolvimento completo (Frontend, Backend, Nginx).
REM Este script funciona no CMD e no PowerShell do Windows.

echo.
echo ==================================================
echo  🚀 Iniciando o ambiente de desenvolvimento...
echo ==================================================
echo.

REM 1. Iniciar o Frontend (Next.js)
echo -> Abrindo nova janela para o Frontend (npm run dev)...
REM Usando o parametro /D para definir o diretorio de trabalho.
start "Frontend - Ride Finance" /D "frontend" cmd /k "npm run dev"

REM 2. Iniciar o Backend (Uvicorn/FastAPI)
echo -> Abrindo nova janela para o Backend (uvicorn)...
REM Ajuste 'app.main:app' se o seu ponto de entrada da aplicacao for diferente.
start "Backend - Ride Finance" /D "backend" cmd /k ".\\venv\\Scripts\\python.exe -m uvicorn app.main:app --reload"

REM 3. Iniciar o Nginx
echo -> Abrindo nova janela para o Nginx (verbose)...
REM Correcao: Passando o argumento com aspas diretamente para o start, que gerencia corretamente.
REM O cmd /k nao e necessario, pois o proprio nginx -g "daemon off;" mantem a janela aberta.
start "Nginx - Ride Finance" /D "nginx" nginx.exe -g "daemon off;"

echo.
echo ==================================================
echo  ✅ Ambiente iniciado! Verifique as 3 novas janelas do CMD que foram abertas.
echo ==================================================
echo.