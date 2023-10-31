import os
import pandas as pd
import numpy as np
import streamlit as st
from src.map_help import BindColormap

# Header and
st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"
                   })
st.header("Pacific Observatory")


st.sidebar.info(
    """
    - See More:
    [Page](https://worldbank.github.io/pacific-observatory/) | [GitHub Repo](https://github.com/worldbank/pacific-observatory)

    """
)

st.markdown(
    """
    [The Pacific Observatory](https://worldbank.github.io/pacific-observatory/) is the World Bank analytical program to explore and develop new information sources 
    to mitigate the impact of data gaps in official statistics for Papua New Guinea (PNG) and the Pacific Island Countries (PICs).
    
    Below is a short description of related pages:
    - **Climate Costs Map** displays the predicted costs for PICs under different adaptation strategies, sea level rise scenarios, and SSP2 in different years.
    - **Solomon Islands News Archive** is a by-product of text analysis in PICs and contains the four major newspapers (SIBC, Solomon Stars, Solomon Times, and The Island Sun) from 2007 to 2023.
"""
)
