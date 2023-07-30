# Cloud Run Python Template

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python](https://img.shields.io/badge/python-3.10.11-blue)](https://www.python.org)

## Installation

```shell
poetry install
```

```shell
poetry shell
```

## Run API Server

```shell
inv start
```

You can send a sample request as below:

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' \
  http://localhost:8080/
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

## Formatter and Linter

### Black

```shell
black --diff --check .
```

### isort

```shell
isort --diff --check .
```

### Flake8

```shell
flake8
```
