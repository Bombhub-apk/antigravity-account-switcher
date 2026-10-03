@echo off
setlocal
cd /d "%~dp0"
echo Launching ChatGPT Desktop Instance 2 (Isolated Account)...
python -c "import chatgpt_account_manager as m; m.launch_chatgpt(instance_num=2)"
timeout /t 2 /nobreak >nul
start /b python chatgpt_cdp_daemon.py
endlocal
