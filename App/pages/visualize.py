from pyrsistent import v
import streamlit as st
import vaex as vx
import numpy
import altair as alt
import pandas as pd
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
from utils import load_data



def app():

    df = load_data()

    st.sidebar.header("Please Filter Here:")
    item = st.sidebar.multiselect("Select Item Class:", options= df['Item_Sub_Category'].unique(), 
            default=df['Item_Sub_Category'].unique()[:5])
    
    facility = st.sidebar.multiselect("Select Facility:", options= df['Sale_Facility'].unique(), 
            default=df['Sale_Facility'].unique()[0])
    
    customer = st.sidebar.multiselect("Select Customer Type:", options= df['Customer_Type'].unique(), 
            default=df['Customer_Type'].unique())

    df_selection = df.to_pandas_df().query("Item_Sub_Category == @item  and Sale_Facility == @facility and Customer_Type == @customer")

    for i in zip(['h', 'D', 'W', 'M'], ['Hourly Rate', 'Daily Rate', 'Weekly Rate', 'Monthly Rate']):
        rate = df_selection.groupby(by=pd.Grouper(key='Sale_Date', freq=i[0])).sum()['Quantity_In_Units']
        # rate.reset_index(inplace=True)
        # rate.rename(columns={'Unnamed: 0':'Sale_Date'}, inplace=True)
        st.subheader(i[1])
        st.dataframe(rate)
        st.line_chart(rate)
        # p = alt.Chart(rate).mark_line().encode(x='Sale_Date', y='Quantity_In_Units')

