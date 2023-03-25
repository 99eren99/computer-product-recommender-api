FROM python:3.10-alpine

VOLUME /usr/src/app/backups

RUN mkdir -p /usr/src/app/backups
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT python3 run.py
