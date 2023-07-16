import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import folium
from streamlit_folium import folium_static
from folium import plugins
from apps import z_functions as zf
def app():
    # title of the app
    options = ['the Sun','the Moon','Polaris','Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    selection = st.selectbox("Celestial Object", options)
    st.markdown(f'Get your position from your direction and altitude to {selection}.')
    if 'h_time' not in st.session_state: st.session_state['h_time'] = datetime.now(timezone.utc)
    h_time = st.session_state['h_time']
    if st.button('Now'):
        h_time = datetime.now(timezone.utc)
    h_time = st.text_input('UTC Time',h_time)
    st.session_state['h_time'] = h_time
    st.write(str(h_time)+'UTC')

    h_az = st.number_input(f'Azimuth degrees to {selection}: ', 0,360,45)
    h_alt = st.number_input(f'Altitude degrees to {selection}: ', 0,90,45)
    

        
        

    