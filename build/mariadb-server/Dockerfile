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
                mariadb-server socat gosu gzip bzip2 openssl vim && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN set -eux; \
    rm -Rf /var/lib/apt/lists/* /var/lib/mysql ; \
    mkdir -p /var/lib/mysql /run/mysqld ; \
    chown -R mysql:mysql /var/lib/mysql /run/mysqld ;

COPY ./script/start.sh /usr/local/bin/start.sh
COPY ./script/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/start.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]

VOLUME /var/lib/mysql
EXPOSE 3306

CMD [ "mariadbd" ]
