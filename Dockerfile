FROM python:3.13-slim

# Evita arquivos .pyc e ativa logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN pip install --no-cache-dir poetry

# Configura Poetry para NÃO criar virtualenv
# (boa prática em container)
RUN poetry config virtualenvs.create false

# Copia apenas arquivos de dependência (cache)
COPY pyproject.toml poetry.lock ./

# Instala dependências
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Copia o restante do código
COPY src ./src

# Expõe a porta da API
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
