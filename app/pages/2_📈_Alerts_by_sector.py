import streamlit as st
from streamlit_utils import *
import plotly.express as px
import pandas as pd


st.set_page_config(page_title="Alerts by sector", page_icon="📈")

add_logos()

df_agg = read_csv_s3("projet-hackathon-ntts-2023/data-hackathon/data_agg_MCC_Month.csv")

df_agg['TxnMonth'] = pd.to_datetime(df_agg['TxnMonth'])

chosen_MCC = st.selectbox(
    'MCC',
    df_agg['MCCGroup'].unique()
)

df_agg_single_MCC = df_agg[df_agg['MCCGroup'] == chosen_MCC]

#st.line_chart(df_agg_single_MCC[['TxnMonth', 'Amount']], x='TxnMonth', y='Amount')

fig = px.line(df_agg_single_MCC.sort_values("TxnMonth"), x="TxnMonth", y="Amount", title=f'Total spend amount - {chosen_MCC}')
st.plotly_chart(fig, theme="streamlit", use_container_width=True)