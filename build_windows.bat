@echo off
echo ===================================================
echo DomainGenerator V2 - Windows Build Script
echo ===================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Building executable with PyInstaller...
pyinstaller --noconfirm --onedir --windowed --name "DomainGenerator" "domain_generator_gui.py"
if errorlevel 1 (
    echo Error: PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo You can find the executable in the "dist\DomainGenerator" folder.
echo.
pause
