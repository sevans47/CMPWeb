import streamlit as st
import requests


api_url = 'https://cmpapi-7wc6zc723a-ew.a.run.app/'

response = requests.get(api_url)

pred = response.json()

pred
