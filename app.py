import streamlit as st
import pandas as pd
#import seaborn as sns 
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

def percentage_formatter(x):
    return f'{x * 100:.2f}%'

@st.cache_data
def import_data():
    df= pd.read_csv("boxing_data_cleaned.csv")
    return df

@st.cache_data
def create_league_tables(df):
    top50 = df.loc[df.Rank<=50,:].value_counts('Country',dropna = False).reset_index().rename(columns = {0:'Top 50'})
    top100 = df.loc[df.Rank<=100,:].value_counts('Country',dropna = False).reset_index().rename(columns = {0:'Top 100'})
    top200 = df.loc[df.Rank<=200,:].value_counts('Country',dropna = False).reset_index().rename(columns = {0:'Top 200'})
    total_fights = df.groupby('Country').agg({'Total Fights':"sum"}).reset_index()
    median_fights = df.groupby('Country').agg({'Total Fights':"median"}).reset_index().rename(columns = {'Total Fights':'Median number of fights'})
    win_record = df.groupby('Country').agg({'Win Percentage':"mean"}).reset_index().rename(columns = {'Win Percentage':'Mean win percentage'})
    
    all_league_tables = (pd.DataFrame(top200.Country.unique(),columns = ['Country'])
                            .merge(top50, how= 'left')
                            .merge(top100, how= 'left')
                            .merge(top200, how= 'left')
                            .merge(total_fights, how= 'left')
                            .merge(median_fights, how= 'left')
                            .merge(win_record, how= 'left')
                            .fillna(0)
                            .astype({'Top 50': 'int32',
                                    'Top 100': 'int32',
                                    'Top 200': 'int32',
                                    'Total Fights': 'int32',
                                    'Median number of fights': 'int32',
                                    'Mean win percentage': 'int32'
                                    }
                                    )
                            .set_index('Country')
                            )
    
    return all_league_tables

def n_top_boxers(league_table):
    return league_table.loc[league_table['Top 200']>0,['Top 50','Top 100','Top 200',]]

def other_league_stats(league_table):
    return league_table.drop(columns = ['Top 50','Top 100','Top 200'])
# =======================================

df = import_data()

"# Comparing pro boxers across countries"
"**Author: Thomas Manandhar-Richardson**"
"Created by scraping the top 1000 male, ranked, professional boxers data from https://boxrec.com/. The data was scraped on a particular day in late 2022 and is not updated."

show_data = st.checkbox("**Click to see the raw the data**")

if show_data:
    chosen_cols = ['Rank','Name','Wins','Losses','Draws','Total Fights','Weight Class','Age','Location']
    df.loc[:,chosen_cols]

col1, col2= st.columns([1,2])

with col1:
    '## Number of top boxers by country'
    'Countries with no fighters in the top 200 were excluded.'
    st.dataframe(n_top_boxers(create_league_tables(df)))
    
    '## Other stats by country'
    st.dataframe(other_league_stats(create_league_tables(df)))
    

with col2: 
    '## Where are the top fighters found?'
    'Each fighter is a single dot placed around the centre of the country they "fight out of" (Finer grained location WIP)'
    st.map(df)


