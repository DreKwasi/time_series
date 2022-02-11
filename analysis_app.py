
import vaex as vx
import dask.dataframe as dd
import pandas as pd
import numpy as np
import os
from datetime import datetime
from dateutil import parser
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
from scipy.signal import savgol_filter
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.stattools import acf, pacf
from sklearn.model_selection import ParameterGrid
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import plotly_express as px
import streamlit as st
import altair as alt

path = os.getcwd()
st.set_page_config(page_title="Pharma Sales Analysis", page_icon=":bar_chart", layout="wide")

st.markdown("""
This app performs Time Series Analysis on ***Pharma Sales Data***!
* **Python libraries:** datetime, pandas, streamlit, numpy, vaex
* **Data source:** [metabase]).
""")

st.sidebar.header('User Input Features')


# Imports data
@st.cache(allow_output_mutation=True)
def load_data(data=path):
    data = vx.open('%s//Data//consumption_data.csv.hdf5'%path)

    # Place all Column Names in a List
    col_names = data.get_column_names()
    # Renaming all columns to fit Vaex standards
    for i in col_names:
       data.rename(i,i.replace(" ", "_").replace("-","_"))

    col_names = data.get_column_names()
# Filtering Data to relevant Columns
    df = data.copy()[[col_names[2], col_names[4], col_names[5], col_names[6], 
                col_names[9], col_names[10], col_names[11], col_names[12], col_names[13],
                col_names[14], col_names[15],col_names[41], col_names[43], col_names[44], col_names[50]]]

# Sort Time Series
    df = df.sort(by='Sale_Date', ascending=True)
    return df


df = load_data('%s//Data//consumption_data.csv.hdf5'%path)


st.sidebar.header("Please Filter Here:")
customer = st.sidebar.multiselect("Select Customer Type:", options= df['Customer_Type'].unique(), 
        default=df['Customer_Type'].unique())

facility = st.sidebar.multiselect("Select Facility:", options= df['Sale_Facility'].unique(), 
        default=df['Sale_Facility'].unique())
        
item = st.sidebar.multiselect("Select Item Class:", options= df['Item_Sub_Category'].unique(), 
        default=df['Item_Sub_Category'].unique())


df_selection = df.to_pandas_df().query('''Customer_Type == @customer and Sale_Facility == @facility and Item_Sub_Category == @item''')

st.header(f"Sales Data Showing {df_selection.shape[0]} rows and {df_selection.shape[1]} columns")
st.warning('Filter On the Left Adjusts the Rows and Columns of the Dataset')
st.write(df_selection)

for i in zip(['H', 'D', 'W', 'M'], ['Hourly Rate', 'Daily Rate', 'Weekly Rate', 'Monthly Rate']):
    rate = df_selection.groupby(by=pd.Grouper(key='Sale_Date', freq=i[0])).sum()
    rate.reset_index(inplace=True)
    rate.rename(columns={'Unnamed: 0':'Sale_Date'}, inplace=True)
    st.subheader(i[1])
    p = alt.Chart(rate).mark_line().encode(x='Sale_Date', y='Quantity_In_Units')

    st.write(p)


# fig_hourly_sales = px.line(
#     sales_by_hour['Quantity_In_Units'],
#     x=sales_by_hour.index,
#     y="Quantity_In_Units",
#     title="<b>Sales by hour</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )

# fig = px.line(        
#         rate, #Data Frame
#         x = rate.index, #Columns from the data frame
#         y = "Quantity_In_Units",
#     title="<b>Sales by monthly</b>",
#     color_discrete_sequence=["#0083B8"] * len(rate),
#     template="plotly_white")

# # fig.update_traces(line_color = "blue")
# st.plotly_chart(fig)

# # left_column = st.columns(1)
# # st.plotly_chart(fig_hourly_sales, use_container_width=True)

