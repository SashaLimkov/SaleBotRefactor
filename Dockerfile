FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR ./src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

COPY . .
