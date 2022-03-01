import streamlit as st
import requests

api_url = 'http://127.0.0.1:8000/'

response = requests.get(api_url)

pred = response.json()

pred
