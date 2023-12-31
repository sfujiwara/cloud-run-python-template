# FROM python:3.10.11-slim
FROM python:3.10.11

# Setup Poetry.
RUN pip install -U pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install Python dependencies.
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install

COPY server server

CMD uvicorn server.main:app --host 0.0.0.0 --port ${PORT}
