import streamlit as st 
from streamlit_folium import st_folium
import folium 
from folium.plugins import MarkerCluster
from folium.plugins import MiniMap
from folium.plugins import MousePosition
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colorbar import ColorbarBase
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from numpy import nan

# Streamlit App Title
app_title = "Oxide values of geologic sample locations 🗺️ 📌"

# Streamlit App Description
app_description = """
Welcome! With this app you can explore oxide values of geologic samples 
from the Banda Arc craton. The sample locations will be displayed on the map, 
distinguished by markers in various colors that correspond to their respective oxide content"""

# Display the title and description
st.title(app_title)
st.markdown(app_description)


# 1. DATA------------------------------------
### read in data
#read in a data files !! In some data files columns are written in capital letters!
df = pd.read_csv('data/Banda Arc.csv')

#GET LOCATIONS –––––––––––––––––––––––––––––––––––––––-
## Extract latitude and longitude columns
latitude = df['LATITUDE MIN']
longitude = df['LONGITUDE MIN']

#INTERACTIVE ELEMENT ––––––––––––––––––––––––––––––––––––––––––––––
option = st.selectbox(
   "Select an oxide of which you would like to display the content.",
   ('TiO2', 'Al2O3', 'FeOT', 'CaO', 'MnO', 'Na2O', 'MGO'),
   index=0,
   placeholder="oxide (wt%)", 
)

df_values = df[option.upper()+'(WT%)'][np.logical_not(np.isnan(df[option.upper()+'(WT%)']))]
st.write('You selected:', df_values)
# SHOW IN VIDEO
#st.write(df[option.upper()+'(WT%)'])
st.write('The min and max values are:', df[option.upper()+'(WT%)'].min(), df[option.upper()+'(WT%)'].max())

st.write('The oxide contents are shown by different colors referred to the colorbar. When you hover over the marker you can see the exact value. Clicking on one marker shows you which oxide you have selected, in case you have forgotten ;). HAVE FUN EXPLORING!!!')


# 2. COLORGRADIENT -------------------------------------------------

# Custom list of hex color codes
custom_colors = ['#FF0000', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF']

# Create a LinearSegmentedColormap from the custom colors
cmap = LinearSegmentedColormap.from_list('CustomGradient', custom_colors, N=len(custom_colors)*10)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(1,6))

#####
# Create a ScalarMappable to map values to colors, show for different oxides
norm = plt.Normalize(df[option.upper()+'(WT%)'].min(), df[option.upper()+'(WT%)'].max())
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
#####

# Add the color bar to the plot
cbar = plt.colorbar(sm, orientation='vertical', ax=ax)
cbar.set_label('Color Bar')

# Hide the axis
ax.set_axis_off()

# 3. MAP--------------------------------------------------------
#Creates a map that centers at "location=", with a zoom of "zoom_start" and a scale bar
      #could add: tiles='Stamen Terrain' to show a terrain map but the attribution is broken
map01 = folium.Map(location=[-10.0,130.00], zoom_start=3, control_scale=True)

#Adds coordinates in markers to map
marker_cluster = MarkerCluster().add_to(map01)  
for lat, lon, i in zip(latitude,longitude,df_values): 
      folium.Marker(location=[lat, lon],
            tooltip = i, 
            popup=option, 
            icon=folium.Icon(
                  color='gray', 
                  icon_color= mcolors.to_hex(cmap(norm(i)), keep_alpha=False), 
                  prefix='fa', 
                  icon='circle')).add_to(marker_cluster)


#SOME EXTRAS –––––––––––––––––––––––––––––––––––––––––––––––
#Adds a search field
folium.plugins.Geocoder().add_to(map01)
#Adds a mini map for overview
MiniMap(toggle_display=True).add_to(map01)
#Shows the gps of your cursor
MousePosition(position="topright",
    separator=" | ",
    prefix="Mouse position:",
    empty_string="NaN").add_to(map01)


## MAP OUTPUT ––––––––––––––––––––––––––––––––––––––––––––––––––––––
col1, col2 = st.columns([0.7, 0.3])
with col1:
     st_folium(map01)


with col2:
      st.pyplot(fig)

