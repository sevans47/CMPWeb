FROM python:3.8.6-buster

COPY setup.py /setup.py
COPY setup.sh /setup.sh
COPY requirements.txt /requirements.txt
COPY web.py /web.py
COPY Procfile /Procfile

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD sudo add-apt-repository ppa:mscore-ubuntu/mscore-stable
CMD sudo apt-get update
CMD sudo apt-get install musescore
