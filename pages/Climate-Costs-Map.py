import os
import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pydeck as pdk


# Specify the filepath and read
cc_file = os.getcwd() + "/data/cc_trimmed.csv"
shp_file = os.getcwd() + "/data/gadm_pacific/"
info_file = os.getcwd() + "/data/country_info.csv"


@st.cache_data
def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path).drop("Unnamed: 0", axis=1)
    return df

df = load_data(cc_file)
info = load_data(info_file)
shp = gpd.read_file(shp_file)

@st.cache_data
def merge_info(_info_data, _geo_data):
    info_data = info.merge(shp[["GID_1", "geometry"]], how="left",
                    left_on="adm1", right_on="GID_1")
    return info_data
info = merge_info(info, shp)

# Specify options
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

    gdp_control = st.toggle("Show GDF Per Capita")

# Apply Filter
df = df[(df.year == select_time) & (df.case == adaptation_option) & (
    df.ssp == ssp_option) & (df.scenario == sea_level_option)].reset_index(drop=True)
df = df.merge(info, how="left", on="adm1")
gdf = gpd.GeoDataFrame(df)
gdf["gdp_pcp"] = gdf["K_2019"]/gdf["pop_2019"]


# Create Map
m = folium.Map(location=(4, 160), zoom_start=4)

# cost_interval = mapclassify.EqualInterval(gdf["total_cost"]).bins.tolist()
# cm1 = linear.YlOrRd_05.scale(0, gdf["total_cost"].max())
# cm1.to_step(index=cost_interval)
# cl = folium.GeoJson(data=gdf,
#                     style_function=lambda x: {
#                         "fillColor": cm1(x["properties"]["total_cost"]),
#                         "fillOpacity": 0.5,
#                         "weight": 1},
#                     popup=folium.GeoJsonPopup(fields=["adm1", "total_cost", "inundation"],
#                                               aliases=["Admin1", "Total Cost", "Inundation"]),
#                     tooltip=folium.GeoJsonTooltip(fields=["total_cost", "K_2019", 'protection', 'relocation', 'stormCapital', 'stormPopulation', 'wetland'],
#                                                   aliases=["Total Costs", "GDP in 2019", "Protection",
#                                                            "Relocation", "Storm Capital", "Storm Population", " Wetlad"],
#                                                   labels=True),
#                     name="Climate Change Costs")
# gdp_interval = mapclassify.EqualInterval(gdf["gdp_pcp"]).bins.tolist()
# cm2 = linear.YlGn_05.scale(0, gdf["gdp_pcp"].max())
# cm2.to_step(index=gdp_interval)
# gl = folium.GeoJson(data=gdf,
#                     style_function=lambda x: {
#                         "fillColor": cm2(x["properties"]["gdp_pcp"]),
#                         "fillOpacity": 1,
#                         "weight": 1},
#                     # popup=folium.GeoJsonPopup(fields=["adm1", "total_cost", "inundation"],
#                     #                           aliases=["Admin1","Total Cost", "Inundation"]),
#                     tooltip=folium.GeoJsonTooltip(fields=["adm1", "gdp_pcp"],
#                                                   aliases=[
#                                                       "Admin1", "GDP per Capita in 2019"],
#                                                   labels=True),
#                     name="GDP Per Capita",
#                     overlay=False)

# m.add_child(cl).add_child(gl)
# m.add_child(folium.LayerControl())
# m.add_child(cm1).add_child(cm2)
# m.add_child(BindColormap(cl, cm1).add_child(BindColormap(gl, cm2)))


gdf.explore(
    tiles="OpenStreetMap",
    column='total_cost',
    tooltip=['total_cost_num', "K_2019", 'inundation', 'protection',
             'relocation', 'stormCapital', 'stormPopulation', 'wetland'],
    cmap="YlOrRd",
    scheme='equalinterval',
    m=m,
    popup=['total_cost_num', "K_2019", 'inundation', 'protection',
           'relocation', 'stormCapital', 'stormPopulation', 'wetland'],
    legend=True,
    legend_kwds=dict(colorbar=True, caption='Total Cost', interval=True, fmt="{:,.0f}",
                     legend_position='topleft'),
    name="Climate Change Costs",
    overlay=True,
    show=True
)

if gdp_control:
    gdf.explore(
        m=m,
        tiles="OpenStreetMap",
        column='gdp_pcp',
        tooltip=["adm1", 'total_cost_num', "gdp_pcp"],
        cmap="PuBu",
        scheme='equalinterval',
        popup=False,
        legend=True,
        legend_kwds=dict(colorbar=True, caption='GDF Per Capita', interval=True, fmt="{:,.0f}",
                        legend_position='topright'),
        name="GDF Per Capita",
        overlay=True
    )

folium.LayerControl().add_to(m)
 

with right_panel:
    folium_static(m, width=1085)