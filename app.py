import streamlit as st
import pandas as pd


df= pd.read_csv("boxing_data.csv")

st.write("Hello world")

st.dataframe(df)
