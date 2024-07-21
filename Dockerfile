FROM python:3

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry

RUN poetry install --no-dev

COPY . .