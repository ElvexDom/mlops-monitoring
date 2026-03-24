# Utilisation d'une image Debian basée sur Python 3.11
FROM python:3.11-slim-bookworm

# Installation de uv depuis l'image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configuration pour installer dans le Python système du conteneur
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

# Copie des fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installation des dépendances
RUN uv pip install --system --no-cache -r pyproject.toml

# Copie du code source
COPY . .

# Exposition du port par défaut
EXPOSE 8501

# Lancement de l'application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]