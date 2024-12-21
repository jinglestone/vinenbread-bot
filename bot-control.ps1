# bot-control.ps1

param (
    [Parameter(Position=0)]
    [string]$Command
)

$pidFile = "bot.pid"

function Start-Bot {
    if (Test-Path $pidFile) {
        Write-Host "⚠️  Бот уже запущен!" -ForegroundColor Yellow
        return
    }
    
    Start-Process -NoNewWindow python -ArgumentList "bot.py"
    $botProcess = Get-Process python | Where-Object { $_.CommandLine -like '*bot.py*' }
    if ($botProcess) {
        $botProcess.Id | Out-File $pidFile
        Write-Host "✅ Бот успешно запущен в фоновом режиме" -ForegroundColor Green
    }
}

function Stop-Bot {
    if (-not (Test-Path $pidFile)) {
        Write-Host "ℹ️  Бот не запущен" -ForegroundColor Blue
        return
    }
    
    $pid = Get-Content $pidFile
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Remove-Item $pidFile
    Write-Host "🛑 Бот остановлен" -ForegroundColor Red
}

function Get-BotStatus {
    if (Test-Path $pidFile) {
        Write-Host "🟢 Бот активен" -ForegroundColor Green
    } else {
        Write-Host "⭕ Бот не запущен" -ForegroundColor Red
    }
}

switch ($Command) {
    "start"  { Start-Bot }
    "stop"   { Stop-Bot }
    "status" { Get-BotStatus }
    default {
        Write-Host "Использование:"
        Write-Host ".\bot-control.ps1 start  - Запустить бота"
        Write-Host ".\bot-control.ps1 stop   - Остановить бота"
        Write-Host ".\bot-control.ps1 status - Проверить статус бота"
    }
}