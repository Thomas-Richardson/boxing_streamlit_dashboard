import streamlit as st
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt


# Server
df= pd.read_csv("boxing_data.csv")

# UI
st.dataframe(df)
