import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium import plugins

from apps import z_functions as zf

def app():
    # title of the app
    lu = st.sidebar.text_input('Lookup: ') 
    if len(lu)>=3:
        where = zf.lookup(lu)
        st.sidebar.write(where[0])
        st.sidebar.write('Lat: '+str(where[1])+' Lon: '+str(where[2]))
        st.sidebar.write('MGRS: '+where[3])
        alt = zf.elevation(where[1],where[2])
        st.sidebar.write('Alt :'+str(round(alt,2))+' Meters')

    c1,c2 = st.columns((1,2))
    with c1:
        if 'a_ipmgrs' not in st.session_state: st.session_state['a_ipmgrs'] = '36JTM1996188760'
        ipmgrs = st.session_state['a_ipmgrs']
        ipmgrs = st.text_input('Impact Point (MGRS):','36JTM1996188760')
        st.session_state['a_ipmgrs'] = ipmgrs
      
        ip = zf.MGRS2LL(ipmgrs)
        st.write('(LL): '+str(round(ip[1],3))+', '+str(round(ip[2],5)))

    with c2:
        # map
        map = folium.Map(location=[ip[1], ip[2]], zoom_start=10)
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
        pal = folium.features.CustomIcon('Icons/paladin.jpg',icon_size=(30,20))
        tgt = folium.features.CustomIcon('Icons/target.png',icon_size=(25,25))

        folium.Marker(location=[ip[1],ip[2]], color='green',popup=ipmgrs, tooltip='Impact Point',icon=tgt).add_to(map)

        

        
        
        draw = plugins.Draw()
        draw.add_to(map)
        # display map
        folium_static(map) 
        

            
    
        
        
        
        
        
        
        
        
        