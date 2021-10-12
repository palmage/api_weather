FROM python:3.9.1

WORKDIR /code
COPY requirements.txt .
RUN pip install -r ./requirements.txt && apt-get update && apt-get install -y nano
COPY . .