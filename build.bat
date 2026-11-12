@echo off
echo Instalando as bibliotecas...
python -m pip install -r requirements.txt pyinstaller

echo.
echo Gerando o executavel...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PickingUpTrash --add-data "assets;assets" main.py

echo.
echo Pronto! O jogo esta em: dist\PickingUpTrash.exe
pause
