FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y  --no-install-recommends --no-install-suggests \
    build-essential pkg-config default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./auth_requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/auth_requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]