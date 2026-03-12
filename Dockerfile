ARG BASE_TAG=stable-apache
FROM nextcloud:${BASE_TAG}

RUN apt update && \
    apt install -y --no-install-recommends --no-install-suggests ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
