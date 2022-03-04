# a little overkill but need it to install dot cli for dtreeviz
FROM ubuntu:18.04

# ubuntu installing - python, pip, graphviz
RUN apt-get update &&\
    apt-get install python3.7 -y &&\
    apt-get install python3-pip -y &&\
    # apt-get install graphviz -y &&\
    apt-get install -y timidity &&\


WORKDIR /streamlit-docker

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY web.py /web.py

CMD streamlit run web.py --server.port $PORT
