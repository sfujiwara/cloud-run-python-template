# Cloud Run Python Template

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org)
[![GitHub Actions](https://github.com/sfujiwara/cloud-run-python-template/actions/workflows/config.yaml/badge.svg)](https://github.com/sfujiwara/cloud-run-python-template/actions/workflows/config.yaml)

## Installation

```shell
uv sync
```

## Run API Server

```shell
uv run inv start
```

You can send a sample request as below:

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' \
  http://localhost:8000/
```

## Deployment

To deploy your application to Cloud Run, you have to edit [`invoke.yaml`](invoke.yaml) (or create another [Invoke](https://github.com/pyinvoke/invoke) config file) for your Google Cloud Platform project.

### Build Docker Image

```shell
inv docker-build -f invoke.yaml
```

You can try the Docker image with `inv docker-run -f invoke.yaml` command.

### Push Docker Image to Artifact Registry

```shell
inv docker-push -f invoke.yaml
```

### Deploy to Cloud Run

```shell
inv deploy -f invoke.yaml
```

## Linter

```shell
uv run ruff check
```

## Formatter

```shell
uv run ruff format --diff
```
