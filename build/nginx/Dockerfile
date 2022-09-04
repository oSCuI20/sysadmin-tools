FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends gnupg dirmngr && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
                dialog apt-utils procps net-tools wget ca-certificates \
                nginx supervisor fcgiwrap python3 gzip bzip2 openssl vim && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN set -eux; \
    apt-get update && \
    apt-get upgrade --no-install-recommends --no-install-suggests -y

EXPOSE 80
EXPOSE 443

RUN mkdir -p /var/log/supervisor

CMD [ "/usr/bin/supervisord" ]
