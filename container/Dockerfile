FROM python:slim

ENV MICROBLOG_STORAGE="/storage"
ENV MICROBLOG_STORAGE_KEY="/storage.key"
ENV GIT_SSH="/usr/local/bin/gitssh"
ENV GIT_SSH_ARGS="-i ${MICROBLOG_STORAGE_KEY} -o StrictHostKeyChecking=no"
ENV ENTRYPOINT="/usr/local/bin/entrypoint"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY --chmod=0555 container/gitssh ${GIT_SSH}
COPY --chmod=0555 container/entrypoint ${ENTRYPOINT}
ADD . /src
RUN pip --no-cache-dir install /src && \
    rm -rf /src

ENTRYPOINT ${ENTRYPOINT}
