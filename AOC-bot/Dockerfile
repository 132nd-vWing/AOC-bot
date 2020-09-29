FROM alpine:latest

WORKDIR /app
ADD requirements.txt /app/

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
            python3-dev \
            py3-pip \
            musl-dev \
            gcc && \
    pip install -r requirements.txt && \
    rm requirements.txt

ADD *.py /app/

CMD ["python3", "main.py"]
