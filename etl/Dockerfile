FROM python:3.10-slim-buster

RUN mkdir -p /usr/src/etl
WORKDIR /usr/src/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "load_data.py"]
