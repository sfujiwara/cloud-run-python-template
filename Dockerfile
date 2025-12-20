FROM python:3.13.7

WORKDIR /app

# Install uv.
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Setup Python packages.
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync --locked

COPY server server
COPY tasks.py tasks.py

ENV PORT=8080

SHELL ["/bin/bash", "-c"]

CMD uv run uvicorn server.main:app --host 0.0.0.0 --port ${PORT}
