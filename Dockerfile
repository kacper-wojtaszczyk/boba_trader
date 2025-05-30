FROM python:3.11-slim AS base

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

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

RUN pip install poetry

WORKDIR /usr/src/app

COPY . .

WORKDIR /usr/src/app

RUN poetry install --all-extras
