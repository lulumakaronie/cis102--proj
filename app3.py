######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static


######################
# Page Title
######################
pricemin = 0
pricemax = 100
# PIL.Image
image = Image.open('ft-logo.png')

#https://docs.streamlit.io/library/api-reference/media/st.image
st.image(image, use_column_width=False)

st.write("""
# Airebnb App

This app, (an Airbnb knockoff called Airebnb) shows the Airebnb of New York City in relation to various factors to help you decide on purchase

***
""")


@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.header('AireBnB Data NYC (2019-09-12)')
st.dataframe(df.head(10))


st.subheader('Find your place to stay at')

st.markdown("Choose a borough, a neighbourhood and a price range if you want to")

# example from before
#cols = ["name", "host_name", "neighbourhood", "room_type", "price"]
#st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
#st.dataframe(df[st_ms].head(10))#

#print(len(df.columns.tolist())) 
#print (len(list(df.values)[0]))


# list of possible boroughs
a = df.values
entries = a.shape[0] 
boroughs = list(a[:,4])
borough_sum = list(set(boroughs))
        
print ("boroughssssssssssssss")
print (borough_sum)

#selection of boroughs

selectedboroughs = st.multiselect("boroughs", borough_sum, default = boroughs[0])

print (selectedboroughs)

# list of possible neighbourhoods
neighbourhoods = list(a[:,5])
neighbourhoods_sum = []
for i in range (0, entries):
    if boroughs[i] in selectedboroughs:
        neighbourhoods_sum.append (neighbourhoods[i])
neighbourhoods_sum = list(set(neighbourhoods_sum))


print("neighbourhoodsssssssssss")
print(neighbourhoods_sum)

# selection of possible neighbourhood

selectedneighbourhoods = st.multiselect("neighbourhood", neighbourhoods_sum, default = neighbourhoods_sum[0])
#st.dataframe(df[st_ms3].head(10))


# selection of price range with slidebar

pricemin = min(list(a[:, 9]))
print(pricemin)
pricemax = max(list(a[:, 9]))
x = st.slider('price range', help="Please choose a range by sliding through the bar", min_value=pricemin, max_value=pricemax, value=(500, 800))
print (x)
# creation of dataframe

aa = df.values.tolist()

print (list(a)[0])
print(aa[0])

bb =[]
for i in range (len(aa)) :   
    if aa[i][5] in selectedneighbourhoods:
        if aa[i][9] <= x[1] and aa[i][9] >= x[0]:
            bb.append(aa[i])

# for behind the scenes infos on errors and stuff
print(bb)

for i, row in enumerate(bb):
    print(f"Length of row {i}: {len(row)}")

print("Length of columns:", len(df.columns))


print("bbbbbbbbbbbb")
print (df.columns.tolist())
#print(bb)

print (len(bb))

print (type (bb))


# display sentence

st.write(f"""
##### Total {len(bb)} housing rental are found in {selectedneighbourhoods} {selectedboroughs} with price between {x[0]} and  {x[1]} dollar
***
""")

# making dataframe

if bb != 0:
    fullyselected = df.columns.tolist()
    df2 = pd.DataFrame(bb, columns=df.columns.tolist())
    st.dataframe(df2[fullyselected].head(len(bb)))
else:
    st.write ("### No matches")
#print (bb[0])
# display table of results ----- not required
#column = ['id', 'name', 'host_id', 'host_name', 'neighbourhood_group', 'neighbourhood', 'latitude', 'longitude', 'room_type', 'price', 'minimum_nights', 'number_of_reviews', 'last_review', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365']
#if bb != 0:
#    fullyselected = pd.DataFrame(bb, column)

#st.dataframe(df[fullyselected].head(10))


#
#st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
#st.dataframe(df[st_ms].head(10))

print("dfejdiofnfdvöjvfdöbjvföjbn")


st.write("---")



st.header("Where are the properties located?")
st.subheader("On a map")
st.markdown("The following map shows the Airebnbs that fit the critieria")


# Get "latitude", "longitude", "price" for top listings
toplistings = df2[["name", "latitude", "longitude", "price"]]
otherlistings = df2[["host_name", "neighbourhood", "room_type"]]
if len(bb) != 0:
    Top = toplistings.values[0,:]
    m = folium.Map(location=Top[1:-1], zoom_start=16)

    tooltip = "listings for specified attributes"

    for j in range(len(bb)):
        name,lat, lon, price = toplistings.values[j,:]
        hostname, neighbourhood, roomtype = otherlistings.values[j,:]
        folium.Marker(
                (lat,lon), popup=f"""Name:{name}
            Neighborhood: {neighbourhood}

            Host name: {hostname}

            Room type: {roomtype}""" , tooltip=f"Price:{price}"
            ).add_to(m)
    
# call to render Folium map in Streamlit
    folium_static(m)


st.write("---")


