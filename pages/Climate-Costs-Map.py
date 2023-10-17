import os
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(layout="wide")
# Specify the filepath and read
cc_file = os.getcwd() + "/data/cc_cleaned.csv"
shp_file = os.getcwd() + "/data/gadm_pacific/"
info_file = os.getcwd() + "/data/country_info.csv"


@st.cache_data
def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path).drop("Unnamed: 0", axis=1)
    return df


df = load_data(cc_file)
info = load_data(info_file)
shp = gpd.read_file(shp_file)


## Specify options
time_options = df["year"].unique().tolist()
scenario_list = ["ssp245_medium", "High", "Low"]
adaptation_list = ["noAdaptation", "optimalfixed", "protect100", "retreat100"]
# default_sea_level_index = scenario_list.index("ssp245_medium")
# scenario_list = scenario_list[default_sea_level_index:] + scenario_list[:default_sea_level_index]

# Header and
st.header("Climate Costs Map")
left_panel, right_panel = st.columns([0.25, 0.75])

with left_panel:
    select_time = st.select_slider(
        "Which Year",
        options=time_options)

    # Newspaper multi-selection widget
    adaptation_option = st.selectbox(
        'Adaptation strategies',
        adaptation_list)

    ssp_option = st.selectbox(
        "Socioeconomic Growth Model",
        ["SSP2"]
    )

    sea_level_option = st.selectbox(
        "Sea Level Rise Scenario",
        scenario_list,
        label_visibility="visible"
    )

# Apply Filter
df = df[(df.year == select_time) & (df.case == adaptation_option) & (
    df.ssp == ssp_option) & (df.scenario == sea_level_option)].reset_index(drop=True)
df = df.merge(shp[["GID_1", "geometry"]], how="left",
              left_on="adm1", right_on="GID_1")
df = df.merge(info, how="left", on="adm1")
gdf = gpd.GeoDataFrame(df)
select_cols_df = [col for col in df.columns if col not in
                  ["geometry", "GID_1"]]


# Create Map
m = folium.Map(location=(4, 160), zoom_start=4)
gdf.explore(
    column='total_cost',
    tooltip=['total_cost_num', "K_2019", 'inundation', 'protection', 'relocation', 'stormCapital', 'stormPopulation', 'wetland'],
    cmap="YlOrRd",
    m=m,
    scheme='equalinterval',
    popup=True,
    legend_kwds=dict(colorbar=False, caption='Total Cost', interval=True, fmt="{:,.0f}")
)

# folium.GeoJson(data=gdf,
#                style_function=lambda x: {
#                    "fillColor": "red",
#                    "fillOpacity": 0.5,
#                    "weight": 1},
#                tooltip=folium.GeoJsonTooltip(fields=["total_cost_num", "K_2019_num"],
#                                              aliases=["Total Costs",
#                                                       "GDP in 2019"],
#                                              labels=True)).add_to(m)

with right_panel:
    folium_static(m, width=1085)
