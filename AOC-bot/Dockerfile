FROM alpine:3.12

WORKDIR /app
COPY requirements.txt /app/

RUN apk update && \
    apk add --no-cache \
            python3=3.8.5-r0 \
            python3-dev=3.8.5-r0 \
            py3-idna=2.9-r0 \
            py3-chardet=3.0.4-r4 \
            py3-pip=20.1.1-r0 \
            musl-dev=1.1.24-r9 \
            gcc=9.3.0-r2 && \
    pip install -r requirements.txt && \
    rm requirements.txt && \
    apk del --rdepends --purge \
            gcc \
            musl-dev \
            python3-dev \
            py3-pip

USER nobody
COPY *.py /app/
CMD ["python3", "main.py"]
