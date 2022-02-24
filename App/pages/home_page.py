
import vaex as vx
import os
from datetime import datetime
from dateutil import parser
import streamlit as st
from utils import load_data

def app():


        st.markdown("""
        This app performs Time Series Analysis/Forecasting on ***Pharma Sales Data***!
        * **Python libraries:** streamlit, vaex, arima, scipy
        * **Data source:** [metabase].
        """)



        data = load_data()

        df = data.copy()[['Sale_Date', 'Sale_Facility', 'Customer_Type', 'Vdl_Drug_Display_Name',
                        'Unit_Selling_Price_Usd', 'Item_Sub_Category']]

        st.header(f"Data Has {df.shape[0]} rows and {df.shape[1]} columns")

        st.sidebar.header('User Input Features')

        item = st.sidebar.multiselect("Select Item Class:", options= df['Item_Sub_Category'].unique(), 
                default=df['Item_Sub_Category'].unique()[:5])

        facility = st.sidebar.multiselect("Select Facility:", options= df['Sale_Facility'].unique(), 
                default=df['Sale_Facility'].unique()[0])

        customer = st.sidebar.multiselect("Select Customer Type:", options= df['Customer_Type'].unique(), 
                default=df['Customer_Type'].unique())


        # df_selection = df[df['Item_Sub_Category']== @item and df['Sale_Facility'] == facility and df['Customer_Type'] == customer ]
        df_selection = df.to_pandas_df().query("Item_Sub_Category == @item  and Sale_Facility == @facility and Customer_Type == @customer")

        st.subheader(f"Raw Sales Data Showing {df_selection.shape[0]} rows and {df_selection.shape[1]} columns")

        st.warning('Filter On the Left Adjusts the Rows and Columns of the Dataset')
        st.dataframe(df_selection)



