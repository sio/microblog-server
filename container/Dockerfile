FROM python:slim

ENV GIT_SSH="/usr/local/bin/gitssh"
ENV GIT_SSH_ARGS="-i /storage.key"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y git && \
    rm -rf /var/lib/apt/lists/*

ADD . /src
RUN mkdir -p $$(dirname "$GIT_SSH") && \
    cp /src/container/gitssh "$GIT_SSH" && \
    chmod 555 "$GIT_SSH"
RUN pip --no-cache-dir install /src && \
    rm -rf /src

ENTRYPOINT ["microblog"]
