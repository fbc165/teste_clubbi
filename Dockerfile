FROM python:3.14-slim-trixie

ADD . /clubbi_api

WORKDIR /clubbi_api

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE 9900

ENTRYPOINT ["sh", "./entrypoint.sh"]