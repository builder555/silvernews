FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN apt update && pip install poetry && poetry install

EXPOSE 8001

CMD poetry run uvicorn api.main:app --reload --host 0.0.0.0 --port 8001
