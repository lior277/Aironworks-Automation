FROM python:3.12-bookworm AS builder

ADD ./ ./tests
ARG MAIN_FOLDER=./tests
ARG PIP_FILE=${MAIN_FOLDER}/Pipfile
ARG PIP_FILE_LOCK=${MAIN_FOLDER}/Pipfile.lock
COPY /Pipfile ${PIP_FILE}
COPY /Pipfile.lock ${PIP_FILE_LOCK}
WORKDIR ${MAIN_FOLDER}

RUN pip install pipenv
RUN pipenv install
RUN pipenv run playwright install --with-deps
RUN apt-get update && apt-get -y install jq