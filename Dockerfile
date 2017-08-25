FROM alpine:3.6

COPY redsym.py /srv/redsym/

COPY REDsym/ /srv/redsym/REDsym/

RUN apk upgrade --update-cache \

# Install permanent runtime dependencies
&& apk add \
	python3 \
	mariadb-client-libs \

# Install build dependencies required to install the PyPI packages below
&& apk add --virtual build-deps \
	mariadb-dev \
	libc-dev \
	python3-dev \
	gcc \

# Install permanent runtime dependencies from PyPI
&& pip3 install \
	mysqlclient \
	pathvalidate \
	regex \
	ftfy \
	ujson \

# Cleanup
&& apk del build-deps \
&& rm -v /var/cache/apk/*

ENTRYPOINT python3 /srv/redsym/redsym.py update
