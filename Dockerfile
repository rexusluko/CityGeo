FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /citygeo

COPY requirements.txt /citygeo/
RUN pip install -r requirements.txt

COPY . /citygeo