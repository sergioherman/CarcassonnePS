$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name Carcassonne --paths src --distpath dist --workpath build --specpath build src/main.py
Write-Host "Pronto: dist\Carcassonne.exe"
