import streamlit as st
from streamlit_utils import *
import plotly.express as px
import pandas as pd


st.set_page_config(page_title="Methodology", page_icon="📖")

st.title("📖 Methodology")

add_logos()

st.image('../hackathon-ntts-2023/logo_midjourney_no_background.png')

st.markdown(
"""
## Panel composition

To control for the growth of the user base, we based our analyses on a panel.

The panel is composed of all users who made at least one transaction in every month from January 2018 to December 2022.

## Alert triggering

Our alert triggering strategy is based on a time series analysis model with, 
available in an open source library called prophet. This approach overcomes the limitations of fixed thresholds

To detect anomalies in a given time series, a model is fit on the series with seasonal adjustment. 
The model generates uncertainty intervals with different levels, and alerts are triggered when the data fall outside these confidence intervals.

## Tools

This application is based on open source tools and packages.

- Data analysis: Python, Spark, R
- Charts: Plotly
- Application: streamlit
- Anomaly detection model: prophet


"""
)