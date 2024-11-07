#!/bin/bash -e

TAG=${RANDOM}

SCRIPT=$1
DATA=$2

docker build --build-arg SCRIPT=${SCRIPT} --build-arg DATA=${DATA}  --platform linux/amd64 . -f Dockerfile -t 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:warning-page${TAG}
docker push 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:warning-page${TAG}

cat base.yaml | DATA_FILE=/testing/data.json SCRIPT=/testing/test.js TAG=warning-page${TAG} envsubst | kubectl apply -f -
