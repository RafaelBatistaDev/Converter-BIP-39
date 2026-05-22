# 🔄 Converter de Números para Frases BIP-39 - converter.py

# Navegar até a pasta
# Executar

## Setup Inicial

```bash
# 1. Cria o toolbox (se for a primeira vez, ele vai baixar a imagem)

``bash
toolbox create 2-Convverter-BIP-39
```

```bash
# 2. Entra no container isolado
toolbox enter 2-Convverter-BIP-39
```

# (Opcional, mas recomendado) Cria um ambiente virtual para isolar ainda mais as libs do projeto
``bash
uv init
uv venv
source .venv/bin/activate
uv sync --all-groups
uv lock
``

``bash
python3 converter.py
```