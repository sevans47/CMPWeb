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

COPY benfacec.jpg /benfacec.jpg
COPY bensheetcol.png /bensheetcol.png
COPY benaudio.wav /benaudio.wav
COPY mizfacec.jpg /mizfacec.jpg
COPY mizsheetcol.png /mizsheetcol.png
COPY mizaudio.wav /mizaudio.wav
COPY stefacec.jpg /stefacec.jpg
COPY stesheetcol.png /stesheetcol.png
COPY steaudio.wav /steaudio.wav
COPY arrange_ben.wav /arrange_ben.wav
COPY arrange_mizuki.wav /arrange_mizuki.wav
COPY arrange_stephen.wav /arrange_stephen.wav
COPY MiniMozartStreamlitStephen.py /MiniMozartStreamlitStephen.py

CMD streamlit run MiniMozartStreamlitStephen.py --server.port $PORT
