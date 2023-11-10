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

RUN apk update && apk add --no-cache bash curl clang git libssl-dev make pkg-config

COPY poetry.lock pyproject.toml ./
COPY boba_trader ./boba_trader

RUN poetry install --only main --all-extras

RUN poetry build -f wheel
RUN python -m pip install ./dist/*whl --force --no-deps

# Final application image
FROM base as application

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
