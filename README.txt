## Configuração do ambiente

O projeto utiliza **Python 3.11** e um ambiente virtual (`venv`).

### Instalação

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Rodar o jogo

```powershell
python src/main.py
```

### Rodar os testes

```powershell
python -m unittest discover -s src/testes -t src
```

### Gerar o executável (Windows)

```powershell
.\gerar_executavel.ps1
```

O arquivo `dist\Carcassonne.exe` é autônomo: não precisa de Python, do código nem de nenhuma
pasta de imagens. Basta enviar esse único arquivo. Na primeira abertura, o Windows pode mostrar o aviso
"O Windows protegeu o computador", porque o executável não é assinado. Para abrir, clique em
"Mais informações" e depois em "Executar assim mesmo".

O PyInstaller só gera executável para o sistema em que roda. Para macOS ou Linux, rode o mesmo
comando do PyInstaller (veja `gerar_executavel.ps1`) numa máquina com esse sistema.
