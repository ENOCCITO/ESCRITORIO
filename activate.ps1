# Script para activar el entorno virtual en Windows (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

.\.venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar la aplicación:" -ForegroundColor Yellow
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Para instalar dependencias:" -ForegroundColor Yellow
Write-Host "  pip install -r requirements.txt" -ForegroundColor White
Write-Host ""
Write-Host "Para desactivar el entorno:" -ForegroundColor Yellow
Write-Host "  deactivate" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
