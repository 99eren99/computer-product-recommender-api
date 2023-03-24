FROM python:3.10-alpine

VOLUME /usr/src/app/backups

RUN mkdir -p /usr/src/app/backups
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN prefect orion start
RUN prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

EXPOSE 4200

RUN python3 flow.py
ENTRYPOINT prefect agent start -q update_products
