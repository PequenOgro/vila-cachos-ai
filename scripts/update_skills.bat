@echo off
echo ============================================================
echo   Atualizando Skills de IA (Superpowers e Vercel Skills)...
echo ============================================================

echo.
echo [1/2] Atualizando Skills Globais (obra/superpowers, etc)...
call npx -y skills update -g -y

echo.
echo [2/2] Atualizando Skills do Projeto Local...
call npx -y skills update -p -y

echo.
echo ============================================================
echo   Todas as skills foram verificadas e atualizadas com sucesso!
echo ============================================================
