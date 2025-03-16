ARG DOCKER_TAG_BASE=3.13-bookworm
ARG DOCKER_TAG_SLIM=3.13-slim-bookworm

FROM python:${DOCKER_TAG_BASE} AS base

ENV PROJECT_ROOT="/opt/app/e-comm-onion-arch-django" \
    VENV_PATH="/var/poetry/venv" \
    VIRTUAL_ENV="${VENV_PATH}"

ENV PATH="${VENV_PATH}/bin:${PATH}"

WORKDIR $PROJECT_ROOT

FROM base AS builder

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100

COPY pyproject.toml uv.lock ./
RUN apt-get update \
    && python -m ensurepip --upgrade \
    && python -m pip install --upgrade pip \
    && python -m venv ${VENV_PATH}
RUN pip install uv \
    && uv sync

ARG PORT=9000
ARG USER="app"

FROM python:${DOCKER_TAG_SLIM} AS main

ENV PROJECT_ROOT="/opt/app/e-comm-onion-arch-django" \
    VENV_PATH="/var/poetry/venv" \
    VIRTUAL_ENV="${VENV_PATH}"

ENV PATH="${VENV_PATH}/bin:${PATH}"

WORKDIR $PROJECT_ROOT

# Copy the virtual environment from the builder stage
COPY  --chown=${USER}:${USER}  --from=builder ${VENV_PATH} ${VENV_PATH}

# Copy the application code
COPY --chown=${USER}:${USER} . ${PROJECT_ROOT}

USER ${USER}

ENTRYPOINT ["./docker-entrypoint.sh"]

EXPOSE ${PORT}
