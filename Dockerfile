# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install pandas
RUN pip3 install google-cloud-bigquery

COPY . .

CMD [ "python3", "api.py"]