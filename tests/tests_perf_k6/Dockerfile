FROM 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner

ARG SCRIPT
ARG DATA

COPY ${SCRIPT} /testing/test.js
COPY ${DATA} /testing/data.json
