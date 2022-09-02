FROM debian:11

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y dialog apt-utils procps net-tools

RUN apt-get install --no-install-recommends --no-install-suggests -y perl ca-certificates && \
    apt-get install --no-install-recommends --no-install-suggests -y \
                nginx supervisor fcgiwrap python3 python3-memcache

EXPOSE 80
EXPOSE 443

RUN mkdir -p /var/log/supervisor

CMD [ "/usr/bin/supervisord" ]
