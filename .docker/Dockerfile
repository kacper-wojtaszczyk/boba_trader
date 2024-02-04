FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
ENV PATH="/root/.cargo/bin:$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
    apt-get install -y curl clang git libssl-dev make pkg-config gcc python3-dev && \
    apt-get clean

RUN python3 -m venv $POETRY_HOME && \
    $POETRY_HOME/bin/pip install poetry

FROM base as builder

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

WORKDIR /usr/src/app

COPY ../poetry.lock pyproject.toml ./

RUN poetry install --no-root --only main

FROM base as dev

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

WORKDIR /usr/src/app

COPY .. .

RUN poetry install --all-extras
