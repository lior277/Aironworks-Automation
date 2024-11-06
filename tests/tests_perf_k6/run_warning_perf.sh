#!/bin/bash -e

docker build --platform linux/amd64 . -f Dockerfile.warning -t 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:warning-page12345678
docker push 901127637159.dkr.ecr.eu-central-1.amazonaws.com/k6-runner:warning-page12345678

kubectl apply -f warning_page_run.yaml
