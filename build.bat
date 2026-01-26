@echo off
echo Building MarkdownChanger...
echo.

pyinstaller --onefile --windowed --name MarkdownChanger --icon=NONE markdown_changer.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful!
    echo Executable location: dist\MarkdownChanger.exe
) else (
    echo.
    echo Build failed!
)

pause
