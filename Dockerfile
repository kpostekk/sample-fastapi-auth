FROM python:3.12-alpine AS base

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY pickme.py .

CMD ["poetry", "run", "python", "pickme.py"]