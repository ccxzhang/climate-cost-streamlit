import os
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random

# Specify the filepath and read
cc_file = os.getcwd() + "/data/cc_cleaned.csv"
shp_file = os.getcwd() + "/data/gadm_pacific/"
info_file = os.getcwd() + "/data/country_info.csv"

df = pd.read_csv(cc_file).drop("Unnamed: 0", axis=1)
shp = gpd.read_file(shp_file)
info = pd.read_csv(info_file).drop("Unnamed: 0", axis=1)

scenario_list = df["scenario"].unique().tolist()
adaptation_list = df["case"].unique().tolist()

# Header and
st.header("Climate Costs Map")
left_panel, right_panel = st.columns([2, 8])

with left_panel:
    select_time = st.select_slider(
        "Which Year",
        options=[2030, 2050, 2070, 2090])

    # Newspaper multi-selection widget
    adaptation_option = st.selectbox(
        'Adaptation strategies',
        adaptation_list)

    ssp_option = st.selectbox(
        "Socioeconomic Growth Model",
        ("SSP2", "SSP1", "SSP3", "SSP4", "SSP5")
    )

    sea_level_option = st.selectbox(
        "Sea Level Rise Scenario",
        scenario_list
    )
# Apply Filter
df = df[(df.year == select_time) & (df.case == adaptation_option) & (
    df.ssp == ssp_option) & (df.scenario == sea_level_option)].reset_index(drop=True)
df = df.merge(shp[["GID_1", "geometry"]], how="left",
              left_on="adm1", right_on="GID_1")
df = df.merge(info, how="left", on="adm1")
gdf = gpd.GeoDataFrame(df)

m = folium.Map(location=(4, 160), zoom_start=4)
for _, r in gdf.iterrows():

    gj = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.001).to_json()
    folium.GeoJson(data=gj).add_to(m)
    folium.CircleMarker(
        location=[r["geometry"].centroid.y, r["geometry"].centroid.x],
        radius=1,
        color="blue",
        popup=folium.Popup((
            "Total Cost: ${cost}<br>"
            "GDP in 2019: {gdp}<br>").format(cost=str(r["total_cost"]), gdp=str(r["K_2019"])),
            min_width=200,
            max_width=200)).add_to(m)

with right_panel:
    folium_static(m, width=900)
