FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /travmaksproject

ADD . /travmaksproject

COPY ./requirements.txt /travmaksproject/requirements.txt

RUN pip install -r requirements.txt

COPY . /travmaksproject


