FROM python:3.8.6-buster

COPY setup.py /setup.py
COPY requirements.txt /requirements.txt
COPY web.py /web.py

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
