# Import Libraries
import json
import numpy as np
import pandas as pd
import plotly as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plot
from urllib.request import urlopen


# Read dataset
df = pd.read_pickle("data_sales_dash.pkl")

with st.sidebar:
    # Menambahkan logo pribadi
         st.write("Hello 👋")
         st.image("asset/Toni.png")
         st.write("""Saya Toni Andreas Susanto mempersembahkan Dashboard Analisis Penjualan Supermarket, sebuah alat yang memudahkan menganalisis data perusahaan dengan visualisasi yang mendalam dan interaktif. Mari menemukan berbagai insight dari perusahaan kami.""")
         st.caption('Copyright © Toni Andreas Susanto 2023')
    
# ---------------------------------------------------- ROW 1 ------------------------------
st.write('# Dashboard Analisis Penjualan Supermarket')

st.write("""Analisis ini menggunakan bahasa pemrograman Python dan visualisasi interaktif (Plotly Express). Data yang digunakan adalah
        data penjualan supermarket yang diperoleh dari https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales.""")

# ---------------------------------------------------- ROW 2 ---------------------------------------------

st.write('### 1: Bagaimana Performa (Total, Quantity, Gross Income) Sales Perusahaan dalam Rentang Tertentu?')

# Filter Indicator
choices = st.radio("Pick One Indicator!", ["Total","Quantity", "Gross Income"])

# Filter Date - Input rentang tanggal 
min_date = df['Date'].min()
max_date = df['Date'].max()

start_date, end_date = st.date_input("Pick a Date Range", 
                                     value=[min_date, max_date], 
                                     min_value=min_date, 
                                     max_value=max_date)

# Data dari st.date_input adalah datetime.date jadi sesuaikan dengan datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


# Persiapan Data
trend = filtered_df.groupby("Date")[choices].sum().reset_index()


# Visualisasi
fig_line = px.line(trend, 
              x="Date", 
              y=choices, 
              title=f'The {choices} Value Over Time',
              markers=True,
              color_discrete_sequence=['blue'])

st.plotly_chart(fig_line)


# ---------------------------------------------------- ROW 3 ---------------------------------------------


st.write('### 2: Bagaimana Performa (Total, Quantity, Gross Income) pada Setiap Product Line?')

# Input data
choices1 = st.radio("Pick One Indicator (Bar Chart) !", ["Total", "Quantity", "Gross Income"])

# Persiapan Data
big_pl = df.groupby("Product line")[choices1].sum().reset_index()

# Visualisasi
fig_bar = px.bar(big_pl.sort_values(by=choices1), 
                 x=choices1,
                 y="Product line",
                 title="Total Sales in Each Product Line",
                 color_discrete_sequence=['blue'])

st.plotly_chart(fig_bar)


# ---------------------------------------------------- ROW 4 ---------------------------------------------


st.write('### 3: Bagaimana Persebaran Total Penjualan dalam Hari maupun Jam Tertentu?')

# Persiapan Data
heatmap = df.groupby(['Day of Week','Hour'])['Total'].sum().reset_index()

# Visualisasi
fig_heatmap = px.density_heatmap(heatmap,
                      x="Day of Week",
                      y="Hour",
                      z="Total",
                      title="Distribution of Total Transaction Value in Every Hour and Day",
                      color_continuous_scale='rdbu',
                      nbinsy=len(df['Hour'].unique()))
st.plotly_chart(fig_heatmap, use_container_width=True)


# ---------------------------------------------------- ROW 5 ---------------------------------------------

st.write('### 4: Bagaimana Perbandingan Gender Pembeli di Setiap Product Line?')

# Persiapan Data
gen_cus = pd.crosstab(index=df['Product line'],
                      columns=df['Gender']).reset_index()

pro_cus_melt = pd.melt(gen_cus, 
                       id_vars='Product line', 
                       var_name="Gender", 
                       value_name='Value')

# Visualisasi Data
fig_stack = px.bar(pro_cus_melt,
       x="Product line",
       y="Value",
       title="Comparison of Male and Female Buyers in Each Product Line",
       color="Gender")

st.plotly_chart(fig_stack, use_container_width=True)