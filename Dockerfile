FROM python:3.8.5-slim-buster

WORKDIR /app

RUN useradd -m app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY --chown=app pyproject.toml poetry.lock /app/
RUN poetry install
USER app
COPY --chown=app . /app

CMD ["kopf", "run", "lib/run.py"]
