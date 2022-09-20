FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

RUN export PYTHONPATH=$PYTHONPATH:/usr/local/lib/$ALPINEPYTHON/site-packages:/usr/lib/$ALPINEPYTHON/site-packages

RUN pip install --upgrade pip

COPY ../requirements.txt ../manage.py .

RUN pip install -r requirements.txt

COPY ../budget_app /app/budget_app/
COPY ../FamilyBudget /app/FamilyBudget/