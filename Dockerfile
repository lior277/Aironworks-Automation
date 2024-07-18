FROM python:3.12-bookworm AS builder
# Set build arguments
ADD ./ ./tests
ARG MAIN_FOLDER=./tests
ARG PIP_FILE=${MAIN_FOLDER}/Pipfile
ARG PIP_FILE_LOCK=${MAIN_FOLDER}/Pipfile.lock
# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

# Set work directory and copy necessary files
WORKDIR ${MAIN_FOLDER}
COPY ./tests ./tests
COPY /Pipfile ${PIP_FILE}
COPY /Pipfile.lock ${PIP_FILE_LOCK}

# Install dependencies and required packages
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --system && \
    pipenv run playwright install --with-deps && \
    pipenv run playwright install chrome && \
    apt-get update && apt-get -y install jq && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
