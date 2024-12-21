@echo off
REM commands.bat - Управление Telegram ботом

if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="status" goto status
goto help

:start
if exist bot.pid (
    echo [33m⚠️  Бот уже запущен![0m
    goto end
)
start /min python bot.py
wmic process where "commandline like '%%python bot.py%%'" get processid | findstr /r "[0-9]" > bot.pid
echo [32m✅ Бот успешно запущен в фоновом режиме[0m
goto end

:stop
if not exist bot.pid (
    echo [34mℹ️  Бот не запущен[0m
    goto end
)
for /f %%i in (bot.pid) do taskkill /F /PID %%i > nul 2>&1
del bot.pid
echo [31m🛑 Бот остановлен[0m
goto end

:status
if exist bot.pid (
    echo [32m🟢 Бот активен[0m
) else (
    echo [31m⭕ Бот не запущен[0m
)
goto end

:help
echo Использование:
echo commands start  - Запустить бота
echo commands stop   - Остановить бота
echo commands status - Проверить статус бота

:end