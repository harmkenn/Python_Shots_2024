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
    st.markdown('Get your position from the location of the sun')
    c1,c2 = st.columns((1,3))
    with c1:
        
        setyear = st.number_input('Year: ',1900,2100,2022)
        setmonth = st.number_input('Month: ',1,12,4)
        setday = st.number_input('Day: ',1,31,9)
        sethour = st.number_input('Hour: ',0,23,22)
        setmin = st.number_input('Minute: ',0,59,40)
        setsec = st.number_input('Second: ',0,59,0)
        
        setday = datetime(setyear,setmonth,setday,sethour,setmin,setsec)

        

    with c2:
        if st.button('Now'):
            setday = datetime.now(timezone.utc)
        st.write(str(setday)+'UTC')
        ssloc = zf.subsolar([setday.year,setday.month,setday.day,setday.hour,setday.minute,setday.second])
        sslat = ssloc[0]
        sslon = ssloc[1]
        st.write('Sub Solar Point: '+str(ssloc)+' MGRS: '+zf.LL2MGRS(sslat,sslon)[1])

        azsun = st.number_input('Azimuth to the Sun',0.00,360.00,10.0)
        bazsun = azsun + 180
        vasun = st.number_input('Vertical Angle to the Sun',0.00,90.00,45.00)
        dist = (90-vasun)/360*2*6371*np.pi
        sslatr = sslat*np.pi/180
        sslonr = sslon*np.pi/180
        bazsunr = bazsun*np.pi/180
        delta = dist/6371

        melatr = np.arcsin(np.sin(sslatr)*np.cos(delta)+np.cos(sslatr)*np.sin(delta)*np.cos(bazsunr))
        melat = melatr*180/np.pi
        melonr = sslonr + np.arctan2(np.sin(bazsunr)*np.sin(delta)*np.cos(sslatr),np.cos(delta)-np.sin(sslatr)*np.sin(melatr))
        melon = melonr*180/np.pi
        fmelon = melon
        if fmelon<-180:
            fmelon = fmelon +360
        if fmelon>180:
            fmelon = fmelon -360
        st.write('My Location: '+ str(melat) + ', ' + str(melon)+ 'MGRS: ' + zf.LL2MGRS(melat,melon)[1])
        
        
        # map
        map = folium.Map(location=[0, 0], zoom_start=1)
        # add tiles to map
        attribution = "Map tiles by Google"
        folium.raster_layers.TileLayer('Open Street Map', attr=attribution).add_to(map)
        folium.raster_layers.TileLayer('Stamen Terrain', attr=attribution).add_to(map)
        # Add custom base maps to folium
        folium.raster_layers.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Maps',
                overlay = False,
                control = True
            ).add_to(map)
        folium.raster_layers.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = False,
                control = True
            ).add_to(map)
        folium.raster_layers.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Terrain',
                overlay = False,
                control = True
            ).add_to(map)

        # add layer control to show different maps
        folium.LayerControl().add_to(map)
        
        # plugin for mini map
        minimap = plugins.MiniMap(toggle_display=True)

        # add minimap to map
        map.add_child(minimap)
        
        # add scroll zoom toggler to map
        plugins.ScrollZoomToggler().add_to(map)

        # add full screen button to map
        plugins.Fullscreen(position='topright').add_to(map)
        
        # add marker to map https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free
        sun = folium.features.CustomIcon('Icons/target.png',icon_size=(30,30))
        folium.Marker(location=[sslat, sslon], color='green', tooltip='SubSolar Point',icon=sun).add_to(map)
        pal = folium.features.CustomIcon('Icons/paladin.jpg',icon_size=(30,20))
        folium.Marker(location=[melat, melon], color='green', tooltip='my location',icon=pal).add_to(map)
        folium.PolyLine([[sslat, sslon],[melat,melon]],tooltip='Azimuth').add_to(map)
        draw = plugins.Draw()
        draw.add_to(map)
        # display map
        folium_static(map)

        
        

    