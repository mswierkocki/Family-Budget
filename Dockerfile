FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
    mariadb-dev \
    gcc \
    musl-dev \
    && pip install mysqlclient==1.4.2.post1 \
    && apk del .build-deps \
    && apk add libffi-dev openssl-dev libgcc 

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add gcc musl-dev
RUN mkdir /app

WORKDIR /app

RUN export PYTHONPATH=$PYTHONPATH:/usr/local/lib/$ALPINEPYTHON/site-packages:/usr/lib/$ALPINEPYTHON/site-packages

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
COPY requirements.PROD.txt /app/requirements.PROD.txt
COPY manage.py /app/manage.py

RUN pip install -r requirements.PROD.txt

COPY ./budget_app /app/budget_app/
COPY ./FamilyBudget /app/FamilyBudget/
