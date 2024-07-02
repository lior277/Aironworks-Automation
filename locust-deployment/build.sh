#!/bin/sh

docker build --platform linux/amd64 . -t asia-northeast1-docker.pkg.dev/phishdetectai/locust-image/locust
docker push asia-northeast1-docker.pkg.dev/phishdetectai/locust-image/locust
