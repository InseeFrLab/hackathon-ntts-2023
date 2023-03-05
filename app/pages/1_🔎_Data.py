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
key_indicators = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/MCC_indicators_panel.csv')
ica_retail = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/ica_G47_TOVT.csv')
ica_accomodation = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/ica_I55_TOVT.csv')
ica_food = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/ica_I56_TOVT.csv')
mcc_aggregations = read_csv_s3('projet-hackathon-ntts-2023/data-hackathon/mcc_groups2.csv')

list_MCCs = amount['MCCLabel'].unique()

MCC_G47 = mcc_aggregations.loc[mcc_aggregations['MCC_group2'] == "Retal trade (G47)", 'MCC'].tolist()
MCC_I55 = mcc_aggregations.loc[mcc_aggregations['MCC_group2'] == "Accomodation (I55)", 'MCC'].tolist()
MCC_I56 = mcc_aggregations.loc[mcc_aggregations['MCC_group2'] == "Food and Beverage (I56)", 'MCC'].tolist()

country_chosen = st.radio("Choose a country", ['DE', 'FR', 'AT', 'ES'], horizontal = True)

amount = amount[amount['Merchantcountry'] == country_chosen]
amount_panel = amount_panel[amount_panel['Merchantcountry'] == country_chosen]

group_chosen = st.radio(
    "Choose MCCs",
    ('Select all MCCs', 'Retail trade', 'Accomodation', 'Food and Beverages Service Activities', 'Select specific MCCs'))

chosen_MCCs = list_MCCs

if group_chosen == "Retail trade":
    chosen_MCCs = MCC_G47
elif group_chosen == "Accomodation":
    chosen_MCCs = MCC_I55
elif group_chosen == "Food and Beverages Service Activities":
    chosen_MCCs = MCC_I56
elif group_chosen == 'Select specific MCCs':
    chosen_MCCs = st.multiselect("Choose MCCs", list_MCCs)
    amount = amount[amount["MCCLabel"].isin(chosen_MCCs)]
    amount_panel = amount_panel[amount_panel["MCCLabel"].isin(chosen_MCCs)]

df_pays = key_indicators[(key_indicators['Merchantcountry'] == country_chosen)]

if group_chosen in (['Accomodation', 'Food and Beverages Service Activities', 'Retail trade']):
    amount = amount[amount["MCC"].isin(chosen_MCCs)]
    amount_panel = amount_panel[amount_panel["MCC"].isin(chosen_MCCs)]
    df_mcc_pays = df_pays[(df_pays['MCC'].isin(chosen_MCCs))]
else:
    df_mcc_pays = df_pays[(df_pays['MCCLabel'].isin(chosen_MCCs))]

total_amount = sum(df_pays["amount"])
total_amount_MCC = sum(df_mcc_pays["amount"])
total_online_amount_MCC = sum(df_mcc_pays["OnlineAmount"])
total_number_MCC = sum(df_mcc_pays["number"])

Rate_all = total_amount_MCC*100/ total_amount if total_amount != 0 else np.NaN
Rate_onlline_mcc_chosen = total_online_amount_MCC*100/ total_amount_MCC if total_amount_MCC != 0 else np.NaN
Average_transaction_amount = total_amount_MCC/ total_number_MCC if total_number_MCC != 0 else np.NaN

col1, col2, col3 = st.columns(3)
col1.metric("Share of MCCs in total spending", f"{Rate_all:.1f} %")
col2.metric("Share of online payments", f"{Rate_onlline_mcc_chosen:.1f} %")
col3.metric("Average transaction amount", f"{Average_transaction_amount:.1f} €")

@st.cache_data(ttl=600)
def transform_ica(ica, country_chosen):
    ica['mois'] = pd.to_datetime(ica['date'] + '-01')
    ica = ica[[country_chosen, 'mois']]
    ica = ica.rename(columns={country_chosen: 'indice'})
    ica = ica.sort_values('mois')
    ica['source'] = 'Turnover (Eurostat)'
    ica_mean = ica.loc[ica['mois'].dt.year == 2018, 'indice'].mean()
    ica['indice'] = 100 * ica['indice'] / ica_mean
    return ica

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
    ica_retail = transform_ica(ica_retail, country_chosen)
    dfs_to_merge = [amount, amount_panel, ica_retail]
elif group_chosen == "Accomodation":
    ica_accomodation = transform_ica(ica_accomodation, country_chosen) if country_chosen != 'AT' else None
    dfs_to_merge = [amount, amount_panel, ica_accomodation] if country_chosen != 'AT' else [amount, amount_panel]
elif group_chosen == "Food and Beverages Service Activities":
    ica_food = transform_ica(ica_food, country_chosen) if country_chosen != 'AT' else None
    dfs_to_merge = [amount, amount_panel, ica_food] if country_chosen != 'AT' else [amount, amount_panel]
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