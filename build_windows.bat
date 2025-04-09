cls
cd frontend
pyinstaller --noconfirm main.spec

cd ..\backend
pyinstaller --noconfirm server.spec