FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y dialog apt-utils procps net-tools perl ca-certificates

RUN apt-get install --no-install-recommends --no-install-suggests -y \
                mariadb-server
