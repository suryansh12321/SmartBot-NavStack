@echo off
echo ==========================================
echo    SmartBot NavStack Auto-Installer
echo ==========================================
echo.

echo [1/3] Checking Python dependencies...
pip install SpeechRecognition pyaudio

echo.
echo [2/3] Compiling the C Navigation Engine...
gcc pathfinder.c -o pathfinder.exe
if %errorlevel% neq 0 (
    echo [ERROR] C Compilation failed! Do you have GCC installed?
    pause
    exit /b
)

echo.
echo [3/3] Verifying Database...
if not exist locations.json (
    echo { "charging dock": [0, 0] } > locations.json
    echo Created default locations.json.
)

echo.
echo ==========================================
echo ✅ INSTALLATION COMPLETE! 
echo You can now run 'ask_bot.py' or 'configurator.py'.
echo ==========================================
pause