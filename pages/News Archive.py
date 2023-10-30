import os
import pandas as pd
import numpy as np
import streamlit as st
import datetime
import random

# Header and
st.header("Solomon Islands News Archive")

# Datetime selection widget
start = datetime.date(2007, 4, 14)
end = datetime.datetime.now()

left_panel, right_panel = st.columns([0.25, 0.75])

with left_panel:
    dates_range = st.date_input(
        "Select the date range for news",
        (start, end), start, end,
        format="YYYY.MM.DD",
    )
    select_start, select_end = dates_range

    # Newspaper multi-selection widget
    source_options = st.multiselect(
        'Select Newspaper Source',
        ['SIBC', 'Solomon Star', 'Solomon Times', 'The Island Sun'])


# if len(source_options) == 0:
#     mapped_element = ("sibc", "ss", "st", "tis")
#     select_query = f"SELECT * FROM NEWS WHERE date >= '{select_start}' and date <= '{select_end}' and publisher in {mapped_element};"
# elif len(source_options) == 1:
#     source_option = source_dict_map[source_options[0]]
#     select_query = f"SELECT * FROM NEWS WHERE date >= '{select_start}' and date <= '{select_end}' and publisher == '{source_option}';"
# elif len(source_options) > 1:
#     mapped_element = tuple([source_dict_map[option]
#                            for option in source_options])
#     select_query = f"SELECT * FROM NEWS WHERE date >= '{select_start}' and date <= '{select_end}' and publisher in {mapped_element};"

# # Connect to SQLITE
# conn = sqlite3.connect("si_news_archive.sqlite3")
# cursor = conn.cursor()
# fetched_data = cursor.execute(select_query).fetchall()
# cursor.close()

github_path = "https://raw.githubusercontent.com/worldbank/pacific-observatory/main/data/text/solomon_islands/"
file_list = ["sibc_news.csv", "island_sun_news.csv",
             "solomon_stars_news.csv", "solomon_times_news.csv"]
source_dict_map = {
    "SIBC": "sibc",
    "Solomon Star": "solomon stars",
    "Solomon Times":  "solomon times",
    "The Island Sun":  "island run"
}

df = pd.DataFrame()
for file in file_list:
    temp = pd.read_csv(github_path + file).drop("Unnamed: 0", axis=1)
    source = file.replace("_news.csv", "").replace("_", " ")
    temp["source"] = source
    if df.empty:
        df = temp
    else:
        df = pd.concat([df, temp], axis=0).reset_index(drop=True)

df["date"] = pd.to_datetime(df["date"], format="mixed")
df = (df[(df.date >= pd.to_datetime(select_start)) &
         (df.date <= pd.to_datetime(select_end)) &
         df.source.isin([source_dict_map[i] for i in source_options])]
      .reset_index(drop=True))


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df)


with right_panel:
    if df.empty:
        st.write("No News fulfilled the requirement.")
    else:
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='solomon_islands_news.csv',
        mime='text/csv',
    )
        random_number = random.randint(0, len(df)-1)
        row = df.iloc[random_number, :]
        st.write("An Example News Look Like: ")
        st.text("Title: " + str(row["title"])
                + "\nDate: " + str(row["date"])
                + "\nSource: " + row["source"].upper()
                + "\nURL: " + str(row["url"]))
        st.write(row["news"])
