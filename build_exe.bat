@echo off
echo ========================================
echo Building Image Deduplicator EXE
echo ========================================
echo.

REM 清理之前的构建
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Step 1: Installing dependencies...
pip install -e ".[optional]"

echo.
echo Step 2: Building EXE with PyInstaller...
pyinstaller build_exe.spec --clean

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo The EXE file is located at: dist\image-deduplicator.exe
echo.
echo You can now run: dist\image-deduplicator.exe
echo.
pause
