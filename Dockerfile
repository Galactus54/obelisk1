FROM python:3.8-slim-buster

EXPOSE 8000

ENV POETRY_VERSION=1.1.7
# Do not generate .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Turn off buffering for logging
ENV PYTHONUNBUFFERED 1

RUN pip install "poetry==$POETRY_VERSION"

COPY . .

RUN poetry config virtualenvs.create true \
  && poetry install --no-interaction --no-ansi

WORKDIR /obelisk
