FROM python:3.13.0-alpine

WORKDIR /app/exchange-rates

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt