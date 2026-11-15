# scripts/keep_alive.ps1
# Script PowerShell para iniciar o Keep-Alive Daemon do Render da Vila Cachos

$host.UI.RawUI.WindowTitle = "Vila Cachos AI - Render Keep-Alive"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Vila Cachos AI - Render Keep-Alive (Sem atraso de 1min)" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Iniciando monitoramento a cada 60 segundos..." -ForegroundColor Yellow
Write-Host " Pressione Ctrl+C para encerrar.`n"

python "$PSScriptRoot\keep_alive_render.py" --interval 60
