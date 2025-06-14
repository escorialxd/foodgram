FROM python:3.13

ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE false

RUN apt install libpq-dev gcc

RUN mkdir /app
WORKDIR /app

RUN pip install poetry==1.8.2

ADD pyproject.toml poetry.lock /app/

RUN poetry lock --no-update
RUN poetry install --no-root

ADD . /code