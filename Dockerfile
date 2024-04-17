FROM python:3.12-bookworm as builder

ADD ./ ./tests
ARG MAIN_FOLDER=./tests
ARG PIP_FILE=${MAIN_FOLDER}/Pipfile
ARG PIP_FILE_LOCK=${MAIN_FOLDER}/Pipfile.lock
COPY /Pipfile ${PIP_FILE}
COPY /Pipfile.lock ${PIP_FILE_LOCK}
WORKDIR ${MAIN_FOLDER}
RUN pip install pipenv
RUN pipenv install
RUN pip install playwright==1.42.0
RUN playwright install --with-deps