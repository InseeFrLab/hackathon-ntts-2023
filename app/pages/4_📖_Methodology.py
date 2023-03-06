import streamlit as st
from streamlit_utils import *
import plotly.express as px
import pandas as pd


st.set_page_config(page_title="Methodology", page_icon="📖")

st.title("📖 Methodology")

add_logos()

st.markdown(
"""
## Panel composition

To control for the growth of the user base, we based our analyses on a panel.

The panel is composed of all users who made at least one transaction in every month from January 2018 to December 2022.

## Alert triggering

Our alert triggering strategy is based on a time series analysis model,
available in an open source library called prophet. This approach overcomes the limitations of fixed thresholds.

To detect anomalies in a given time series, a model is fit on the series with seasonal adjustment.
The model generates uncertainty intervals with different levels (90%, 95%, and 99%), and alerts are triggered when the data fall outside these confidence intervals.

### Covid correction

Most of the sectors were highly affected by the Covid-19 pandemic,
leading to series with very unusual values (either too high or too low) for several months.
This inevitably impacts the time series models, resulting in very large confidence intervals.
To account for this, we add a Covid correction when fitting the models.

In practice, in the decomposition of the time series, in addition to the trend and seasonality,
there is a special component for the Covid period. This period was set to March 2020 - May 2021, 
encompassing the major lockdowns in Europe.

## Tools

This application is based on open source tools and packages.

- Data analysis: Python, Spark, R
- Charts: Plotly
- Application: streamlit
- Anomaly detection model: prophet


"""
)
