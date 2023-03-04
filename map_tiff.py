import streamlit as st
from streamlit_folium import folium_static
import folium
import rasterio
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

#st.text(cm.get_cmap('viridis'))
def get_color(x):
    decimals = 2
    x = np.around(x, decimals=decimals)
    ls = np.linspace(0,1,10**decimals+1)
    if 0 <= x <= 1:
        return cm.get_cmap('viridis')(ls)[np.argwhere(ls==x)]
    elif x==-128:
        return (0, 0, 0, 0)
    else:
        raise ValueError()
# A dummy Sentinel 2 COG I had laying around

# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )


#tif = "test.tif"
cmap = ListedColormap(["darkorange", "gold", "lawngreen", "lightseagreen"])
m = folium.Map(location=[12.9716, 77.5946], zoom_start=11)
st.title("Test Application")
uploaded_files = st.sidebar.file_uploader("Please choose a file", type=['tif','tiff','geotiff'],accept_multiple_files=True)
#st.sidebar.text(uploaded_files)

# This is probably hugely inefficient, but it works. Opens the COG as a numpy array
#@st.cache_data
#def main_func():   
for file in uploaded_files:
#if uploaded_files is not None:   
    src = rasterio.open(file.name)
    array = src.read()
    bounds = src.bounds
    #st.sidebar.text(file.read())

    x1,y1,x2,y2 = src.bounds
    bbox = [(bounds.bottom, bounds.left), (bounds.top, bounds.right)]


    

# center on Liberty Bell

# add marker for Liberty Bell
# tooltip = "Manilla city"
# folium.Marker(
#     [14.599512, 120.984222], popup="This is it!", tooltip=tooltip
# ).add_to(m)

    img = folium.raster_layers.ImageOverlay(
    name="Sentinel 2",
    image=np.moveaxis(array, 0, -1),
    bounds=bbox,
    opacity=0.9,
    interactive=True,
    cross_origin=False,
    zindex=1,
    colormap=cmap
    )

# folium.Popup("I am an image").add_to(img)
    img.add_to(m)
    folium.LayerControl().add_to(m)

# call to render Folium map in Streamlit
    folium_static(m)

#main_func()