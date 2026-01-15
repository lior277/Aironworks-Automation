FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app

# Install dependencies first (cached layer)
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy

# Install Playwright and system dependencies
RUN pipenv run playwright install --with-deps && \
    pipenv run playwright install chrome && \
    apt-get update && apt-get -y install jq && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy tests last (changes frequently)
COPY ./tests ./tests