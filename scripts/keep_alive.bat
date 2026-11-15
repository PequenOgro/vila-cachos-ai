@echo off
title Vila Cachos AI - Render Keep-Alive Daemon
echo ========================================================
echo  Vila Cachos AI - Render Keep-Alive (Sem atraso de 1min)
echo ========================================================
echo  Iniciando monitoramento a cada 60 segundos...
echo  Para pausar/fechar, feche esta janela ou pressione Ctrl+C.
echo.
python "%~dp0keep_alive_render.py" --interval 60
pause
