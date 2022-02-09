
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

path = os.getcwd()
st.set_page_config(page_title="Pharma Sales Analysis", page_icon=":bar_chart", layout="wide")

# Imports data
data = vx.open('%s//Data//consumption_data.csv.hdf5'%path)

# Place all Column Names in a List
col_names = data.get_column_names()
# Renaming all columns to fit Vaex standards
for i in col_names:
    data.rename(i,i.replace(" ", "_"))
    data.rename(i, i.replace("-","_"))

col_names = data.get_column_names()

# Filtering Data to relevant Columns
df = data.copy()[[col_names[2], col_names[4], col_names[5], col_names[6], 
                col_names[9], col_names[10], col_names[11], col_names[12], col_names[13],
                col_names[14], col_names[15],col_names[41], col_names[43], col_names[44], col_names[50]]]


# Viewing the Relevant Columns
df.get_column_names()
# Sort Time Series
df = df.sort(by='Sale_Date', ascending=True)


st.sidebar.header("Please Filter Here:")
customer = st.sidebar.multiselect("Select Customer Type:", options= df['Customer_Type'].unique(), 
        default=df['Customer_Type'].unique())

facility = st.sidebar.multiselect("Select Facility:", options= df['Sale_Facility'].unique(), 
        default=df['Sale_Facility'].unique())
        
item = st.sidebar.multiselect("Select Item Class:", options= df['Item_Sub_Category'].unique(), 
        default=df['Item_Sub_Category'].unique())


df_selection = df.to_pandas_df().iloc[:2000,:].query('''Customer_Type == @customer and Sale_Facility == @facility and Item_Sub_Category == @item''')

st.dataframe(df_selection)
