FROM alpine:latest

WORKDIR /app
ADD requirements.txt /app/

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
            python3 \
            python3-dev \
            py3-idna \
            py3-chardet \
            py3-pip \
            musl-dev \
            gcc && \
    pip install -r requirements.txt && \
    rm requirements.txt && \
    apk del --rdepends --purge \
            gcc \
            musl-dev \
            python3-dev \
            py3-pip

ADD *.py /app/

CMD ["python3", "main.py"]
