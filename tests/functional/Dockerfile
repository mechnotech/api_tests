FROM python:3.9
RUN apt-get update && apt-get install -y iputils-ping
WORKDIR /tests
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY commands.sh .
COPY ./ ./tests
