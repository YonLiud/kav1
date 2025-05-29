@echo off
cls

for /f %%i in ('git rev-parse --short HEAD') do set GIT_HASH=%%i
echo %GIT_HASH% > frontend\version.txt
echo %GIT_HASH% > backend\version.txt

set RELEASE_BUILD=false

cd frontend
pyinstaller --noconfirm main.spec
cd ..

cd backend
pyinstaller --noconfirm server.spec
cd ..
