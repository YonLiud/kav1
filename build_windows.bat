@echo off
cls

:: Get the current git hash
for /f %%i in ('git rev-parse --short HEAD') do set GIT_HASH=%%i
echo Current git hash: %GIT_HASH%

:: Create version files
echo %GIT_HASH% > frontend\version.txt
echo %GIT_HASH% > backend\version.txt

:: Set build mode
set RELEASE_BUILD=true

:: Build frontend
echo BUILDING FRONTEND
cd frontend
pyinstaller --noconfirm main.spec
cd ..

:: Build backend
echo BUILDING BACKEND
cd backend
pyinstaller --noconfirm server.spec
cd ..

echo Build completed with version: %GIT_HASH%
pause