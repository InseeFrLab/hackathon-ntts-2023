import streamlit as st
import plotly.express as px
import numpy as np
from streamlit_utils import *
import time
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="The dataset", page_icon="🔎")

add_logos()

st.title("🔎 The dataset")

# Daily transactions

df_daily = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/Daily_data.csv')
df_daily=df_daily.sort_values('day')
fig0 = px.line(df_daily, x="day", y="Number", title="Credit card daily transactions")
#st.plotly_chart(fig0, theme="streamlit", use_container_width=True)

chart = st.plotly_chart(fig0, use_container_width=True)
for i in range(len(df_daily)):
    df_subset = df_daily.iloc[:i+1]
    fig0.data[0].x = df_subset['day']
    fig0.data[0].y = df_subset['Number']
    fig0.update_layout(title="Credit card daily transactions")
    chart.plotly_chart(fig0)
    time.sleep(0.001)

# Share of amount by type of payment NO panel data

df_type_payment = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/Cash_Online_offline_nopanel.csv')
df_type_payment=df_type_payment.sort_values('Mois')
df_type_payment.rename(columns = {'Mois':'Month'}, inplace = True)
df_type_payment.sort_values(['Month', 'PaymentType'], inplace = True)
fig1 = px.line(df_type_payment, x="Month", y="ShareAmount",color='PaymentType', title="Share of amount by type of payment - All users")
st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

# Share of amount by type of payment panel data

df_type_payment_pan = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/Cash_Online_offline_panel.csv')
df_type_payment_pan=df_type_payment_pan.sort_values('Mois')
df_type_payment_pan.rename(columns = {'Mois':'Month'}, inplace = True)
df_type_payment_pan.sort_values(['Month', 'PaymentType'], inplace = True)
fig2 = px.line(df_type_payment_pan, x="Month", y="ShareAmount",color='PaymentType', title="Share of amount by type of payment - Panel")
st.plotly_chart(fig2, theme="streamlit", use_container_width=True)


#### Share activity per sector#########


mcc_groups2 = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/mcc_groups2.csv')

amount = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/amount.csv')
amount = amount.merge(mcc_groups2, on="MCC", how="left")
amount = amount.loc[~amount['MCC_group2'].isna()]
amount = amount.groupby('MCC_group2').agg(amount=('amount', 'sum')).reset_index()
amount['amount_rate'] = 100 * amount['amount'] / amount['amount'].sum()
amount = amount.sort_values('amount_rate', ascending=False)

amount_panel = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/amount_panel.csv')
amount_panel = amount_panel.merge(mcc_groups2, on="MCC", how="left")
amount_panel = amount_panel.loc[~amount_panel['MCC_group2'].isna()]
amount_panel = amount_panel.groupby('MCC_group2').agg(amount=('amount', 'sum')).reset_index()
amount_panel['amount_rate'] = 100 * amount_panel['amount'] / amount_panel['amount'].sum()
amount_panel = amount_panel.sort_values('amount_rate', ascending=False)

# Créer le graphique donut chart
fig1 = go.Figure(data=[go.Pie(labels=amount['MCC_group2'],
                             values=amount['amount_rate'],
                             hole=.5)])
fig1.update_layout(title='Share of amount by great sectors - all users',
                  annotations=[dict(text=' ',
                                    font_size=20,
                                    showarrow=False)])

# Créer le graphique donut chart
fig2 = go.Figure(data=[go.Pie(labels=amount_panel['MCC_group2'],
                             values=amount_panel['amount_rate'],
                             hole=.5)])
fig2.update_layout(title='Share of amount by great sectors - panel',
                  annotations=[dict(text=' ',
                                    font_size=20,
                                    showarrow=False)])

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with col2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)



#####################

# Share of amount by age group NO panel data

df_age_no = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/agegroup_nopanel.csv')
df_age_no =df_age_no.sort_values('AgeGroup')
fig3 = px.bar(df_age_no, x='AgeGroup', y='ShareAmount', title="Share of amount by age group - All users")
#st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

# Share of amount by age group panel data

df_age_pan = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/agegroup_panel.csv')
df_age_pan =df_age_pan.sort_values('AgeGroup')
fig4 = px.bar(df_age_pan, x='AgeGroup', y='ShareAmount', title="Share of amount by age group - Panel")
#st.plotly_chart(fig4, theme="streamlit", use_container_width=True)


col1, col2 = st.columns(2)
with col1 : 
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
with col2 :
    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)


# heatmap NO panel  country

data=[[63, 35, 0, 0, 1], [1, 98, 0, 0, 1], [2, 34, 58, 1, 5],[1, 29, 2, 43, 25]]
fig6 = px.imshow(data,
                labels=dict(x="User country", y="Merchant country", color="Amount share"),
                x=['Austria', 'Deutschland', 'Spain', 'France', 'Other'],
                y=['Austria', 'Deutschland', 'Spain', 'France'],
                text_auto=True,
                title='Share of amount - All users'
               )
fig6.update_xaxes(side="top")
st.plotly_chart(fig6, theme="streamlit", use_container_width=True)

# heatmap panel  country

data=[[59, 40, 0, 0, 1], [1, 98, 0, 0, 1], [4, 89, 3, 2, 2],[2, 47, 0, 47, 4]]
fig5 = px.imshow(data,
                labels=dict(x="User country", y="Merchant country", color="Amount share"),
                x=['Austria', 'Deutschland', 'Spain', 'France', 'Other'],
                y=['Austria', 'Deutschland', 'Spain', 'France'],
                text_auto=True,
                title='Share of amount - Panel'
               )
fig5.update_xaxes(side="top")
st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

# col1, col2 = st.columns(2)
# with col1 : 
#     st.plotly_chart(fig6, theme="streamlit", use_container_width=True)
# with col2 :
#     st.plotly_chart(fig5, theme="streamlit", use_container_width=True)


# Map : Share of accommodation expenditures in total spending

st.subheader('Share of accommodation expenditures in total spending')

map_html = read_html_s3('projet-hackathon-ntts-2023/data-hackathon/map_accomadation_expenditures_rate_nuts3_v2.html')
st.components.v1.html(map_html, height=700)
