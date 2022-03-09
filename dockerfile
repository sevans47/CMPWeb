FROM python:3.8.6-buster
RUN apt-get update
RUN apt-get install -y timidity
RUN apt-get install -y fluidsynth
RUN apt-get install -y musescore
RUN apt-get install -y lilypond
RUN pip install --upgrade pip

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY blank.png /blank.png
COPY melodywriter.py /melodywriter.py
RUN mkdir /usr/share/soundfonts
COPY UprightPiano.sf2 /usr/share/soundfonts/default.sf2

CMD streamlit run melodywriter.py --server.port $PORT
