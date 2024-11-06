#!/bin/bash -e

TAG=${RANDOM}

docker build --platform linux/amd64 . -f Dockerfile.warning -t 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:education-perf${RANDOM}
docker push 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:education-perf${RANDOM}

cat education_content_run.yaml | TAG=${RANDOM} envsubst | kubectl apply -f -
