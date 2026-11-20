# update_skills.ps1
# Atualiza automaticamente todas as skills globais e de projeto do ecossistema de IA

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Atualizando Skills de IA (obra/superpowers e vercel-labs) " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`n[1/2] Atualizando Skills Globais (obra/superpowers, etc)..." -ForegroundColor Yellow
npx -y skills update -g -y

Write-Host "`n[2/2] Atualizando Skills do Projeto Local..." -ForegroundColor Yellow
npx -y skills update -p -y

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  Todas as skills estao atualizadas com sucesso!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
