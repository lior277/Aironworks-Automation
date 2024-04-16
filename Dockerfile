FROM python:3.12-bookworm as builder

ADD ./ ./tests
ARG MAIN_FOLDER=./tests
COPY / ${MAIN_FOLDER}
WORKDIR ${MAIN_FOLDER}
RUN pip install pipenv
RUN pipenv install && pipenv sync

