FROM python:3.11.5-slim

WORKDIR /code

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python
ENV POETRY_VERSION=1.8.2 PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock* /code/
RUN poetry install --no-root

COPY . .