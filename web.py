import streamlit as st
import requests
import music21

api_url = 'https://cmpapi-7wc6zc723a-ew.a.run.app'


response = requests.get(api_url)

pred = response.json()

st.write(pred)
