FROM python:3.13

ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE false

RUN apt-get update \
&& apt-get -y install g++ libpq-dev gcc unixodbc unixodbc-dev

RUN pip install psycopg2

RUN mkdir /app
WORKDIR /app

RUN pip install poetry==1.8.2

ADD pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-cache

ADD . /code