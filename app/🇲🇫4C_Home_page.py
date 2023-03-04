import streamlit as st
from streamlit_utils import add_logos

st.set_page_config(
    page_title="4C: Control credit card consumption",
    page_icon="🇲🇫",
)

st.title("4C: Control credit card consumption :flag-mf:")

st.write("This application leverages granular card payments data to provide interactive data visualisation. It also provides alerts to detect sudden changes in consumer spending for a wide range of sectors.")

add_logos()
