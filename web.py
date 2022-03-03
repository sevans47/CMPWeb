import streamlit as st
import requests
from music21 import converter, environment

# api_url = 'https://cmpapi-7wc6zc723a-ew.a.run.app'


# response = requests.get(api_url)

# pred = response.json()

# st.write(pred)

#hopoefuly it'll work
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = '/app/usr/bin/mscore3'
us['musicxmlPath'] = '/app/usr/bin/mscore3'

s = converter.parse('tinyNotation: 4/8 C4_hi D-4 E#4 F8 trip{G4 A4 B4} c4')
s.show()
s.show('midi')

st.write('hello')
st.write('hi')
