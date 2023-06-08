import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium import plugins
import numpy as np
from scipy.optimize import curve_fit
import plotly.express as px
from apps import z_functions as zf
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def app():
    # title of the app
       
    st.markdown('AFATDS')
    c1,c2,c3 = st.columns((1,3,1.5))
    with c1:
        lu = st.sidebar.text_input('Lookup: ') 
        if len(lu)>=3:
            where = zf.lookup(lu)
            st.sidebar.write(where[0])
            st.sidebar.write('Lat: '+str(where[1])+' Lon: '+str(where[2]))
            st.sidebar.write('MGRS: '+where[3])
            alt = zf.elevation(where[1],where[2])
            st.sidebar.write('Alt :'+str(round(alt,2))+' Meters')
    with c1:
        if 'd_lpmgrs' not in st.session_state: st.session_state['d_lpmgrs'] = '29NQH5872754513'
        d_lpmgrs = st.session_state['d_lpmgrs']
        d_lpmgrs = st.text_input('Launch Point (MGRS):',d_lpmgrs, key = 'd1')
        st.session_state['d_lpmgrs'] = d_lpmgrs
        
        lp = zf.MGRS2LL(d_lpmgrs)
        st.write('Launch Point (LL):') 
        st.write(str(round(lp[1],5))+', '+str(round(lp[2],5)))

        if 'd_lpalt' not in st.session_state: st.session_state['d_lpalt'] = 123
        d_lpalt = st.session_state['d_lpalt']
        d_lpalt = st.text_input('Launch Altitude (M):',d_lpalt, key = 'd3')
        st.session_state['d_lpalt'] = d_lpalt

        if 'd_ipmgrs' not in st.session_state: st.session_state['d_ipmgrs'] = '29NQH4843150392'
        d_ipmgrs = st.session_state['d_ipmgrs']
        d_ipmgrs = st.text_input('Imoact Point (MGRS):',d_ipmgrs, key = 'd2')
        st.session_state['d_ipmgrs'] = d_ipmgrs

        ip = zf.MGRS2LL(d_ipmgrs)
        st.write('Impact Point (LL):')
        st.write(str(round(ip[1],5))+', '+str(round(ip[2],5)))

        if 'd_ipalt' not in st.session_state: st.session_state['d_ipalt'] = 321
        d_ipalt = st.session_state['d_ipalt']
        d_ipalt = st.text_input('Impact Altitude (M):',d_ipalt, key = 'd4')
        st.session_state['d_ipalt'] = d_ipalt

        if 'd_AOF' not in st.session_state: st.session_state['d_AOF'] = 0
        d_AOF = st.session_state['d_AOF']
        d_AOF = st.text_input('Azimuth of Fire (mils):',d_AOF, key = 'd5')
        st.session_state['d_AOF'] = d_AOF 
        
    if len(d_lpmgrs)>3 and len(d_ipmgrs)>3:
        
        with c1:
            deets = zf.P2P(lp[1],lp[2],ip[1],ip[2])
            st.write('Distance: ' + str(round(deets[2],0)) + ' meters')
            st.write('Launch Bearing: '+str(round(deets[0],2)) + ' degrees')
            st.write('Launch Azimuth: '+str(round(deets[0]*3200/180,2)) + ' mils')
            st.write('Impact Bearing: '+str(round(deets[1],2)) + ' degrees')
            st.write('Impact Azimuth: '+str(round(deets[1]*3200/180,2)) + ' mils')
        with c2:
            # map
            map = folium.Map(location=[(lp[1]+ip[1])/2, (lp[2]+ip[2])/2], zoom_start=-1.36*np.log(deets[2]/1000)+15)
            # add tiles to map
            folium.raster_layers.TileLayer('Open Street Map').add_to(map)
            folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
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
                    iles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
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
            folium.Marker(location=[lp[1],lp[2]], color='green',popup=d_lpmgrs, tooltip='Launch Point',icon=pal).add_to(map)
            folium.Marker(location=[ip[1],ip[2]], color='green',popup=d_ipmgrs, tooltip='Impact Point',icon=tgt).add_to(map)
            

            
        with c2:
            points = []
            points.append([lp[1],lp[2]])
            for p in range(1,101):
                get = zf.polar2LL(lp[1],lp[2],deets[0],deets[2]*p/100000)
                points.append([get[0],get[1]])
            points.append([ip[1],ip[2]])
            folium.PolyLine(points, color='red').add_to(map)
            
            
        
            
            draw = plugins.Draw()
            draw.add_to(map)
            # display map
            folium_static(map) 
        with c3:
            rng = round(deets[2],0)
            chrg = st.selectbox('Charge:',['Auto','1L','2L','3H','4H','5H'])
            if chrg == 'Auto':
                chrg = pd.cut([rng], bins=[-1,2000,5000,8000,12000,15000,25000,99999999], labels=['Too Short','1L','2L','3H','4H','5H','Too Far'])
                chrg = chrg[0]

            ning = int(d_lpmgrs[-5:])
            if ning > 1000:
                ring = ning - 1000
                sp = d_lpmgrs[:-5]+str(ring).rjust(5, "0")
            else:
                ring = ning + 1000
                sp = d_lpmgrs[:-5]+str(ring).rjust(5, "0")
            spll = zf.MGRS2LL(sp)
            gd = zf.P2P(spll[1],spll[2],lp[1],lp[2])

            gdm = gd[0]/180*3200
            if gdm > 4800:
                gdm = gdm - 6400
            if gdm > 1600:
                gdm = gdm - 3200

            macs = pd.read_csv('data/M795Macs.csv')

            #macs = macs[macs['Chg'].str.contains(chrg[-2:])]
            
            # Load data from CSV file
            
            macs['cosAZ'] = np.cos(macs['GTL (mils)']*np.pi/3200)
            macs = macs.loc[macs['Chg'] == chrg]

            # Extract the feature and target variables
            X = macs[['Range (M)', 'cosAZ', 'Galt (M)','Talt (M)']]
            y = macs[['Drift', 'QE (mils)', 'TOF', 'MAX Ord (M)']]
            
            # Creating polynomial features
            
            poly_features = PolynomialFeatures(degree=3)
            input_features_poly = poly_features.fit_transform(X)

            # Creating and training the polynomial regression model
            model = LinearRegression()
            model.fit(input_features_poly, y)
            
            new_data = pd.DataFrame({'Range (M)':[rng], 'cosAZ':[deets[0]*np.pi/180], 'Galt (M)':[d_lpalt],'Talt (M)':[d_ipalt]})
            new_input_features_poly = poly_features.transform(new_data)
            output = model.predict(new_input_features_poly)
            st.write(new_data)
            st.write(output)
            
            mo = output[0,3]
            qe = output[0,1]
            tof = output[0,2]
            drift = output[0,0]
            defl = 3200 + int(d_AOF) - deets[0] *3200/180 + drift + gdm
            if defl<0: defl = defl + 6400
                        
            data = pd.DataFrame({'Range (Meters)':str(int(rng)),
                                 'Shell':'M795','Charge':chrg, 'Azimuth to Target (mils)':str(round(deets[0]*3200/180,0)),
                                 'Grid Declination (mils)':str(round(gdm,1)),'Drift (mils)':str(round(drift,1)),'Deflection (mils)':str(round(defl,1)),
                                 'Muzzle Velocity (m/s)':str(macs.iat[1,7]),
                                 'QE (mils)':str(round(qe,1)),
                                 'Time of Flight (sec)':str(round(tof,1)),
                                 'MaxOrd (Meters)':str(round(mo,0))},index = ['Fire Mission']).T 
            st.dataframe(data,height=500) 
           
        with c2:
            
            tPoints = pd.DataFrame({'Ranges':[0,.1*rng,.60*rng,.61*rng,rng],'Alts':[int(d_lpalt),.15*rng*np.tan(qe/3200*np.pi),mo,mo,int(d_ipalt)]})
           
            x, y = tPoints['Ranges'], tPoints['Alts']
            model5 = np.poly1d(np.polyfit(x, y, 5))
            x_traj = np.arange(0, int(rng), 100)
            y_traj = model5(x_traj)
            fig = px.scatter(tPoints, x=x_traj, y=y_traj)
            fig.update_layout(autosize=False,width=700,height=mo/rng*800*2.5)
            st.plotly_chart(fig)

 
            
            
            
            


        
    