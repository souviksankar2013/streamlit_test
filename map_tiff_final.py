import streamlit as st
import os
from streamlit_folium import folium_static
import folium
import rasterio
import numpy as np
from matplotlib import cm
import tempfile
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#import matplotlib.pylab as pl

import pylandstats as pls
from pylandstats import Landscape as ld
import geopandas as gpd
import pandas as pd
import altair as alt



cmap = ListedColormap(["red", "red",'yellow','white'])
m = folium.Map(location=[30.316496, 78.032188], zoom_start=11)
st.title("Landscape Matrices Calculation")




patch_option = ('No of Patches')
area_option = ('Area Metric 1','Area Metric 2')
landscape_option = ('Land Metric 1','Land Metric 2')


def value_select():
    option1 = st.sidebar.empty()

    if (option == 'Patch'):
    #option1.selectbox('Choose Patch Metric Type?',patch_option)
        option1.selectbox('Choose Patch Metric Type?',patch_option)

    elif (option == 'Area'):
        option1.selectbox('Choose Area Metric Type?',area_option)

    elif (option == 'Landscape'):
        option1.selectbox('Choose Landscape Metric Type?',landscape_option)


option = st.sidebar.selectbox('Choose Land Metric Type?',('Patch','Area','Landscape'),on_change=value_select)



uploaded_files = st.sidebar.file_uploader("Please choose a file", type=['tif','tiff','geotiff'],accept_multiple_files=True)

    

#st.write('You selected:', option1)


patch_number=[]
year=[]

for file in uploaded_files:

  tempfile1 = tempfile.NamedTemporaryFile(delete=False,suffix='.tif')
  tempfile1.write(file.getbuffer())
  src = rasterio.open(tempfile1.name)
  array = src.read()
  bounds = src.bounds
  x1,y1,x2,y2 = src.bounds
  bbox = [(bounds.bottom, bounds.left), (bounds.top, bounds.right)]

  img = folium.raster_layers.ImageOverlay(
    name=file.name,
    image=np.moveaxis(array, 0, -1),
    bounds=bbox,
    opacity=0.9,
    interactive=True,
    cross_origin=False,
    zindex=1,
    colormap=cmap
    )
  img.add_to(m)

  #matrix Calculation
  ls = pls.Landscape(tempfile1.name)
  class_metrics_df = ls.compute_class_metrics_df(metrics=['proportion_of_landscape', 'edge_density' , 'total_area' , 'number_of_patches' ,'landscape_shape_index' ])
  #st.write(list(class_metrics_df['number_of_patches'])[0])
  patch_number.append(list(class_metrics_df['number_of_patches'])[0])

  file_name = file.name
  year.append(file_name.split('_')[1])

folium.LayerControl().add_to(m)
folium_static(m)


chart_data = pd.DataFrame({
                  'no_of_patches': patch_number,
                   'year': year
                })

chart_data = chart_data.set_index('year')
#st.write(np.array(patch_number).shape)
#st.write(np.array(year).shape)

#chart_data.reset_index(drop=True, inplace=True)
st.line_chart(chart_data)
#chart_data.plot()


# chart = alt.Chart(
#             data=chart_data,
#             title="Your title",
#         ).mark_line().encode()

# st.altair_chart(chart)