FROM python:3.9.0rc1-alpine3.12

COPY docker-entrypoint.sh /

RUN    apk --no-cache add --virtual=.build-dep build-base git cmake \
    && apk --no-cache add zeromq-dev libffi-dev \
    && python3 -m pip install locust==2.27.0 \
    && apk del .build-dep \
    && chmod +x /docker-entrypoint.sh \
    && mkdir /locust
WORKDIR /locust
EXPOSE 8089 5557 5558

ENTRYPOINT ["/docker-entrypoint.sh"]
