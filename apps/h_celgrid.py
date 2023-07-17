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
    if 'h_time' not in st.session_state: st.session_state['h_time'] = datetime.now(timezone.utc)
    h_time = st.session_state['h_time']
    if st.button('Now'):
        h_time = datetime.now(timezone.utc)
    h_time = st.text_input('UTC Time',h_time)
    st.session_state['h_time'] = h_time
    st.write(str(h_time)+'UTC')

    h_az = st.number_input(f'Azimuth degrees to {selection}: ', 0,360,45)
    h_alt = st.number_input(f'Altitude degrees to {selection}: ', 0,90,45)

    if selection == 'the Sun': 
        # Define the observed altitude and azimuth of the Sun
        observed_altitude = np.radians(45.0/180*np.pi)  # degrees to radians
        observed_azimuth = np.radians(190.0/180*np.pi)  # degrees to radians

        # Create an Observer object
        observer = ephem.Observer()
        observer.lat = '0'  # Set observer's latitude (in this case, 0 degrees)
        observer.lon = '0'  # Set observer's longitude (in this case, 0 degrees)
        observer.elev = 0  # Set observer's elevation (in this case, sea level)
        observer.date = ephem.now()  # Set the current date and time

        # Compute the observer's location based on the observed altitude and azimuth of the Sun
        sun = ephem.Sun()
        sun_altitude = observed_altitude
        sun_azimuth = observed_azimuth
        sun.compute(observer)
        sun_altitude_diff = sun.alt - sun_altitude
        sun_azimuth_diff = sun.az - sun_azimuth

        # Update the observer's position based on the computed differences
        observer.lat += sun_altitude_diff
        observer.lon += sun_azimuth_diff

        # Extract the observer's latitude and longitude
        observer_latitude = np.degrees(observer.lat)
        observer_longitude = np.degrees(observer.lon)

        # Print the computed observer's location
        st.write("Computed Observer's Latitude:", observer_latitude)
        st.write("Computed Observer's Longitude:", observer_longitude)

    elif selection == 'the Moon': out = 'Moon is up'
    else: out = 'Something else'
    
   
    


        
        

    