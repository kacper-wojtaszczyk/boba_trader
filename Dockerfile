FROM python:3.11-alpine as base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    BUILD_MODE="release"
ENV PATH="/root/.cargo/bin:$POETRY_HOME/bin:$PATH"
WORKDIR $PYSETUP_PATH

FROM base as builder

# Install build deps
RUN apk update && apk add --no-cache bash curl clang git libssl-dev make pkg-config

# Install Rust stable and poetry
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    curl -sSL https://install.python-poetry.org | python3 -

# Install package requirements (split step and with --no-root to enable caching)
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --only main

COPY nautilus_trader ./nautilus_trader
RUN poetry install --only main --all-extras
RUN poetry build -f wheel
RUN python -m pip install ./dist/*whl --force --no-deps
RUN find /usr/local/lib/python3.11/site-packages -name "*.pyc" -exec rm -f {} \;

# Final application image
FROM base as application

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages