import streamlit as st
import pandas as pd
#import seaborn as sns 
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

def import_data():
    df= pd.read_csv("boxing_data_cleaned.csv")
    return df

def create_league_tables(df):
    top50 = df.loc[df.Rank<=50,:].value_counts('Country',dropna = False).reset_index().rename(columns = {0:'Top 50'})
    top100 = df.loc[df.Rank<=100,:].value_counts('Country',dropna = False).reset_index().rename(columns = {0:'Top 100'})
    top200 = df.loc[df.Rank<=200,:].value_counts('Country',dropna = False).reset_index().rename(columns = {0:'Top 200'})

    all_league_tables = (pd.DataFrame(top200.Country.unique(),columns = ['Country'])
                            .merge(top50, how= 'left')
                            .merge(top100, how= 'left')
                            .merge(top200, how= 'left')
                            .fillna(0)
                            .astype({'Top 50': 'int32',
                                    'Top 100': 'int32',
                                    'Top 200': 'int32'}
                                    )
                            )
    all_league_tables.loc[all_league_tables.Country != 0,:]
    return all_league_tables

# =======================================

df = import_data()

"# Comparing pro boxers across countries"
"**Author: Thomas Manandhar-Richardson**"
"Created by scraping the top 1000 male, ranked professional boxers data from https://boxrec.com/. The data was scraped on a particular day in late 2022 and is not updated."

show_data = st.checkbox("**Click to see the raw the data**")

if show_data:
    chosen_cols = ['Rank','Name','Wins','Losses','Draws','Total Fights','Weight Class','Age','Location']
    df.loc[:,chosen_cols]

col1, col2= st.columns([1,2])

with col1:
    '## Number of top boxers by country'
    'Countries with no fighters in the top 200 were excluded.'
    create_league_tables(df)

with col2: 
    '## Where are the top fighters found?'
    'Each fighter is a single dot placed around the centre of the country they "fight out of" (Finer grained location WIP)'
    st.map(df)


