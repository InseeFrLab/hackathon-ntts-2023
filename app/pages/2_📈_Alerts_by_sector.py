import streamlit as st
from streamlit_utils import read_csv, read_html, add_logos
import plotly.express as px


st.set_page_config(page_title="Alerts by sector", page_icon = "📈")

add_logos()

df_agg = read_csv("projet-hackathon-ntts-2023/data/data_agg_MCC_Month.csv")
st.dataframe(df_agg)

df_agg['TxnMonth'] = pd.to_datetime(df_agg['TxnMonth'])

chosen_MCC = st.selectbox(
    'MCC',
    df_agg['MCC'].unique()
)

df_agg_single_MCC = df_agg[df_agg['MCC'] == chosen_MCC]

st.line_chart(df_agg_single_MCC[['TxnMonth', 'Amount']], x='TxnMonth', y='Amount')