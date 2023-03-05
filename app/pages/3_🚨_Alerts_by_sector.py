import streamlit as st
from streamlit_utils import *
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import numpy as np


st.set_page_config(page_title="Alerts by sector", page_icon="🚨")

st.title("🚨 Warning system: Alerts by sectors")

add_logos()


df_agg = read_csv_s3("projet-hackathon-ntts-2023/data-hackathon/data_agg_MCC_Month_anomaly_3levels.csv")
#df_95 = read_csv_s3("projet-hackathon-ntts-2023/data-hackathon/data_agg_MCC_Month_anomaly95.csv")
#df_99 = read_csv_s3("projet-hackathon-ntts-2023/data-hackathon/data_agg_MCC_Month_anomaly95.csv")

df_agg['TxnMonth'] = pd.to_datetime(df_agg['TxnMonth'])

chosen_MCC = st.selectbox(
    'Sector',
    df_agg[['MCCGroup', 'Amount']].groupby('MCCGroup').sum('Amount').sort_values('Amount', ascending = False).index
)

df_agg_single_MCC = df_agg[df_agg['MCCGroup'] == chosen_MCC]

#st.line_chart(df_agg_single_MCC[['TxnMonth', 'Amount']], x='TxnMonth', y='Amount')

#st.write(df_agg_single_MCC)

#color_map = {-1: 'red'}

#colors = ['red' if (anomaly != 0) else 'blue' for anomaly in df_agg_single_MCC['anomaly']]
#color_sequence = ['red' if (anomaly != 0) else None for anomaly in df_agg_single_MCC['anomaly']]

#st.write(color_sequence)

#color_sequence = np.where(df_agg_single_MCC['anomaly']==0, 'red', None)

#fig = px.line(df_agg_single_MCC.sort_values("TxnMonth"), x="TxnMonth", y="Amount", 
#title=f'Total spend amount - {chosen_MCC}', markers = True, color_discrete_sequence=color_sequence)
#fig.update_traces(mode='markers+lines')







# create trace for line graph
#line_trace = go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['Amount'], mode='lines+markers')

# create list to hold colors for each point based on 'anomaly' column
#colors = ['red' if (anomaly != 0) else None for anomaly in df_agg_single_MCC['anomaly']]

# update marker attribute of line trace with colors
#line_trace.marker = dict(color=colors)

# create plot and display
#fig = go.Figure(data=[line_trace])

# create dictionary mapping 'anomaly' values to colors
#color_map = {-1: 'red', 0:None}

# create line graph with color based on 'anomaly' column
#fig = px.line(df, x='x', y='y', color='anomaly', color_discrete_map=color_map)

# create line graph
fig = px.line(df_agg_single_MCC.sort_values("TxnMonth"), x="TxnMonth", y="Amount", 
title=f'Total spend amount - {chosen_MCC}')

#99% anomalies
df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == 3]
fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['red']).data[0])
df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == -3]
fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['red']).data[0])

#fig.add_trace(px.scatter(df_agg_single_MCC, x='TxnMonth', y='Amount', color='anomaly').data[0])

#99% confidence intervals
fig.add_trace(go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['yhat_upper99'],
                    line = dict(color='rgba(255,0,0,0.4)', dash='dash')))

fig.add_trace(go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['yhat_lower99'],
                    line = dict(color='rgba(255,0,0,0.4)', dash='dash')))

# 95% anomalies
df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == 2]
fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['orange']).data[0])
df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == -2]
fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['orange']).data[0])

# 95% confidence intervals
fig.add_trace(go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['yhat_upper95'],
                    line = dict(color='rgba(255,69,0, 0.4)', dash='dash')))

fig.add_trace(go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['yhat_lower95'],
                    line = dict(color='rgba(255,69,0, 0.4)', dash='dash')))

# 90% anomalies

df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == 1]
fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['yellow']).data[0])
df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == -1]
fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['yellow']).data[0])

# 90% confidence intervals
fig.add_trace(go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['yhat_upper90'],
                    line = dict(color='rgba(204,204,0, 0.4)', dash='dash')))

fig.add_trace(go.Scatter(x=df_agg_single_MCC['TxnMonth'], y=df_agg_single_MCC['yhat_lower90'],
                    line = dict(color='rgba(204,204,0, 0.4)', dash='dash')))


#df_95['TxnMonth'] = pd.to_datetime(df_95['TxnMonth'])
#df_agg_single_MCC = df_agg[df_agg['MCCGroup'] == chosen_MCC]

#df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == 1]
#fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['orange']).data[0])
#df_filtered = df_agg_single_MCC[df_agg_single_MCC['anomaly'] == -1]
#fig.add_trace(px.scatter(df_filtered, x='TxnMonth', y='Amount', color_discrete_sequence=['orange']).data[0])


fig.update_traces(showlegend=False, marker={'size': 8})

st.plotly_chart(fig, theme="streamlit", use_container_width=True)