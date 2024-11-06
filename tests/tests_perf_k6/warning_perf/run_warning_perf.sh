#!/bin/bash -e

TAG=${RANDOM}

docker build --platform linux/amd64 . -f Dockerfile.warning -t 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:warning-page${RANDOM}
docker push 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:warning-page${RANDOM}

cat warning_page_run.yaml | TAG=${RANDOM} envsubst | kubectl apply -f -
