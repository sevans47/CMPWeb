import streamlit as st
import requests

api_url = 'https://taxifare.lewagon.ai/predict'

response = requests.get(api_url)

pred = response.json()

pred
