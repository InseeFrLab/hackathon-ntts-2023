import streamlit as st
import plotly.express as px
import numpy as np
from streamlit_utils import *


st.set_page_config(page_title="Data", page_icon="🔎")

add_logos()

st.markdown("## Impact of the panel")
st.markdown("The user base is regularly growing. Using a panel enables to control for this growth and compute meaningful indicators that closely match official ones.")

amount = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/amount.csv')
amount_panel = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/amount_panel.csv')
ica_retail = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/ica_G47_TOVT.csv')
ica_accomodation = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/ica_I55_TOVT.csv')
ica_food = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/ica_I56_TOVT.csv')

list_MCCs = amount['MCC'].unique()

country_chosen = st.radio("Choose a country", ['Germany', 'France', 'Austria', 'Spain'], horizontal = True)

group_chosen = st.radio(
    "Choose MCCs",
    ('Select all MCCs', 'Retail trade', 'Accomodation', 'Food and Beverages Service Activities', 'Select specific MCCs'))

chosen_MCCs = list_MCCs

st.write(amount["MCC"])

if group_chosen == "Retail trade":
    chosen_MCCs = [5099,5122,5131,5137,5139,5193,5200,5211,5231,5251,
    5311,5499,5611,5621,5631,5641,5651,5661,5691,5699,5712,5713,5714,
    5719,5722,5732,5735,5912,5931,5941,5942,5943,5944,5946,5948,5963,
    5965,5976,5977,5983,5992,5994,763,5310,5331,5399,5411,5422,5441,
    5451,5499,5921,5993,5541,5542,5172]
elif group_chosen == "Accomodation":
    chosen_MCCs = [7011,7032,7033]
elif group_chosen == "Food and Beverages Service Activities":
    chosen_MCCs = [5811,5812,5813,5814]
elif group_chosen == 'Select specific MCCs':
    chosen_MCCs = st.multiselect("Choose MCCs", list_MCCs)
    amount = amount[amount["MCCLabel"].isin(chosen_MCCs)]
    amount_panel = amount_panel[amount_panel["MCCLabel"].isin(chosen_MCCs)]

if group_chosen in (['Accomodation', 'Food and Beverages Service Activities', 'Retail trade']):
    amount = amount[amount["MCC"].isin(chosen_MCCs)]
    amount_panel = amount_panel[amount_panel["MCC"].isin(chosen_MCCs)]

amount = amount.groupby("mois").agg({"amount": "sum"}).reset_index()
amount["mois"] = pd.to_datetime(amount["mois"].apply(lambda x: x + "-01"))
amount = amount.sort_values("mois").assign(source="All users")
amount_mean = amount[amount["mois"].dt.year == 2018]["amount"].mean()
amount = amount.assign(indice = 100 * amount["amount"] / amount_mean)

amount_panel = amount_panel.groupby("mois").agg({"amount": "sum"}).reset_index()
amount_panel["mois"] = pd.to_datetime(amount_panel["mois"].apply(lambda x: x + "-01"))
amount_panel = amount_panel.sort_values("mois").assign(source="Panel")
amount_panel_mean = amount_panel[amount_panel["mois"].dt.year == 2018]["amount"].mean()
amount_panel = amount_panel.assign(indice = 100 * amount_panel["amount"] / amount_panel_mean)#.drop(columns=["amount"])

dfs_to_merge = []

if group_chosen == "Retail trade":
    #dfs_to_merge = [amount, amount_panel, ica_retail]
    dfs_to_merge = [amount, amount_panel]
elif group_chosen == "Accomodation":
    #dfs_to_merge = [amount, amount_panel, ica_accomodation]
    dfs_to_merge = [amount, amount_panel]
elif group_chosen == "Food and Beverages Service Activities":
    #dfs_to_merge = [amount, amount_panel, ica_food]
    dfs_to_merge = [amount, amount_panel]
else:
    dfs_to_merge = [amount, amount_panel]

merged_df = pd.concat(dfs_to_merge, ignore_index=True)

merged_df = merged_df[merged_df["mois"] <= pd.Timestamp("2022-02-01")]

# tracer le graphique
fig = px.line(merged_df, x="mois", y="indice", color="source", line_group="source",
              hover_name="source", title="Total spendings - Index with 2018 base = 100",
              labels={"mois": "Month", "indice": "Index, 2018 = 100",
                      "source": "Data"})
st.plotly_chart(fig, theme="streamlit", use_container_width=True)