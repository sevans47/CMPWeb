import streamlit as st
import requests
#from music21 import converter, environment
from midi2audio import FluidSynth


# api_url = 'https://cmpapi-7wc6zc723a-ew.a.run.app'


# response = requests.get(api_url)

# pred = response.json()

# st.write(pred)

#hopoefuly it'll work
# us = environment.UserSettings()
# us['musescoreDirectPNGPath'] = '/build_498a5956/usr/bin/mscore3'
# us['musicxmlPath'] = '/build_498a5956/usr/bin/mscore3'

# environment.set('midiPath', '/usr/bin/mscore3')
# s = converter.parse('tinyNotation: 4/8 C4_hi D-4 E#4 F8 trip{G4 A4 B4} c4')
# s.show('midi')


#Lets go


# サウンドフォントを指定する
fs = FluidSynth(sound_font='font.sf2')
# 入力するmidiファイルとアウトプットファイル
fs.midi_to_audio('input.mid', 'output.mp3') # またはoutput.wav


audio_file = open('song/mz_311_1.wav', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')
