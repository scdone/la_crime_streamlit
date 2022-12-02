import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

##### DATA PREP ######

df = pd.read_csv('clean_crime_data.csv')

df.date = pd.to_datetime(df.date)




##### FRONT END ######

st.title('LA Crime Explorer')

selected_year = st.radio('Pick a year to explore', (2020, 2021, 2022))

option = st.selectbox(
    'See crime summary in...', ('Southwest', 'Central', 'N Hollywood')
)


### TOTAL INCIDENTS ###

def get_total(area, selected_year):

    total = len(df[(df['area'] == f'{area}') & (df['date'].dt.year == selected_year)])

    return total

total_incidents = get_total(option, selected_year)
st.markdown(f'<h1 style="color:#EE4B2B">{total_incidents} total incidents</h1>', unsafe_allow_html=True)

### LINE CHART BY MONTH ###

def line_chart(area, selected_year):

    data = df[(df['date'].dt.year == selected_year) & (df['area'] == f'{area}')].groupby(df['date'].dt.month).size().to_frame().reset_index().rename(columns={'date':'month', 0:'count'})
    
    # maximum = data.sort_values('count', ascending=False)[:1]['count'][0]

    data.replace({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 
                    5:'May', 6:'June', 7:'July', 8:'Aug', 
                    9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}, inplace=True)

    fig = px.line(data, x='month', y='count', 
                    labels={'count':'Total Incidents', 'month':'Month'},
                    title=f'By month...')

    # fig.update_layout(yaxis_range=[0, 1800])

    fig.update_yaxes(rangemode="tozero")

    return fig

st.plotly_chart(line_chart(option, selected_year))

#### BAR CHART OF CATEGORIES ####

def bar_chart(option, selected_year):

    data = df[(df['date'].dt.year == selected_year) & (df['area'] == f'{option}')].groupby('category').size().to_frame().reset_index().rename(columns={'category':'Category', 0:'Incidents'}).sort_values('Incidents', ascending=False)[:5]

    fig = px.bar(data, x='Category', y='Incidents')

    return fig


st.plotly_chart(bar_chart(option, selected_year))
