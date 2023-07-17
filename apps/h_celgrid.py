import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import folium
from streamlit_folium import folium_static
from folium import plugins
from apps import z_functions as zf
import ephem
def app():
    # title of the app
    options = ['the Sun','the Moon','Polaris','Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    selection = st.selectbox("Celestial Object", options)
    st.markdown(f'Get your position from your direction and altitude to {selection}.')
    if 'h_time' not in st.session_state: st.session_state['h_time'] = ephem.Date(datetime.now(timezone.utc))
    h_time = st.session_state['h_time']
    if st.button('Now'):
        h_time = ephem.Date(datetime.now(timezone.utc))
    h_time = st.text_input('UTC Time',h_time)
    st.session_state['h_time'] = h_time
    st.write(str(h_time)+'UTC')

    h_az = st.number_input(f'Azimuth degrees to {selection}: ', 0,360,45)
    h_alt = st.number_input(f'Altitude degrees to {selection}: ', 0,90,45)

    observer = ephem.Observer()
    observer.lat = '0'  # Example latitude (London, United Kingdom)
    observer.lon = '0'
    if selection == 'the Sun': 
        cel = ephem.Sun()
    elif selection == 'the Moon': 
        cel = ephem.Moon()
    elif selection == 'Polaris': 
        cel = ephem.star('Polaris') # https://theskylive.com/sky/stars/polaris-alpha-ursae-minoris-star
    elif selection == 'Mercury': 
        cel = ephem.Mercury() # https://theskylive.com/where-is-mercury
    elif selection == 'Venus': 
        cel = ephem.Venus()
    elif selection == 'Mars': 
        cel = ephem.Mars()
    elif selection == 'Jupiter': 
        cel = ephem.Jupiter()
    elif selection == 'Saturn': 
        cel = ephem.Saturn()
    elif selection == 'Uranus': 
        cel = ephem.Uranus()
    elif selection == 'Neptune': 
        cel = ephem.Neptune()
    else: out = 'Something else'
    
    cel.compute(observer)
    cel_azimuth = float(cel.az)*180/np.pi
    cel_altitude = float(cel.alt)*180/np.pi
    st.write(f"{selection}'s Azimuth from 0,0:", cel_azimuth)
    st.write(f"{selection}'s Altitude from 0,0:", cel_altitude)
    cel_dist = 40050*(90-cel_altitude)/360
    st.write(cel_dist)
    sub_cel = zf.polar2LL(0,0,cel_azimuth,cel_dist)
    st.write(f"{selection}'s Sub-Latitude: ", sub_cel[0], f"{selection}'s Sub-Longitude: ", sub_cel[1] )
    


        
        

    