import streamlit as st
from streamlit_utils import *
import plotly.express as px
import pandas as pd


st.set_page_config(page_title="Roadmap", page_icon="🎯")

st.title("🎯 Roadmap")

add_logos()

st.markdown(
"""
This application is in its early stages. We plan to improve it in different ways.

### Improve the panel constitution

- Control for the **age distribution**
- Control for the **user country distribution**

### Add indicators for alert triggerring

In addition to the total spend, the same methodology could be used on other indicators. 
For instance, detecting changes in the **share of a specific sector in the total spend** would bring 
valuable information.

### Fine-tune alerts levels

Currently, the alerts are based on 90\%, 95\% and 99\% confidence intervals. A more thorough 
analysis would help to fine tune these levels to ensure the rate of false alerts stays low while 
minimizing missed anomalies.

### Use daily data to trigger alerts

Our current alert triggering mechanism relies on monthly aggregated data. We could leverage the 
power the daily data by running the anomaly detection on daily data and define a new strategy 
to trigger alerts, for instance when several consecutive days are considered anormal.

### Trigger alerts on a more granular geographical level

Using the same methodology, alerts could be triggered when changes are detected at regional level for instance.




"""
)
