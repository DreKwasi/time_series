from turtle import home
import streamlit as st

# Custom imports 
from multi_page import MultiPage
from pages import home_page, visualize# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.set_page_config(page_title="Pharma Sales Analysis", page_icon=":bar_chart", layout="wide")

st.title("Pharma Sales Forecasting")

# Add all your applications (pages) here
app.add_page("Home", home_page.app)
app.add_page("Visualize", visualize.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()