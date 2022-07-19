FROM python:slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y git && \
    rm -rf /var/lib/apt/lists/*

ADD . /src
RUN pip --no-cache-dir install /src && \
    rm -rf /src

ENTRYPOINT ["microblog"]
