FROM python:slim

ADD . /src
RUN pip --no-cache-dir install /src && rm -rf /src

ENTRYPOINT ["microblog"]
