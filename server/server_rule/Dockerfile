FROM python:latest

RUN python -m pip install psycopg2
RUN pip show psycopg2

ADD server_rule.py /server_rule/

WORKDIR /server_rule/