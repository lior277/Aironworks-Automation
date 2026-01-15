FROM python:3.12-bookworm AS builder

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./
COPY ./tests ./tests

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy && \
    pipenv run playwright install --with-deps && \
    pipenv run playwright install chrome && \
    apt-get update && apt-get -y install jq && \
    apt-get clean && rm -rf /var/lib/apt/lists/*