FROM ubuntu:22.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install Flask requests

WORKDIR /app

COPY . /app

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python3", "app.py"]

