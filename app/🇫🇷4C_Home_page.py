import streamlit as st
from streamlit_utils import add_logos

st.set_page_config(
    page_title="4C: Control credit card consumption",
    page_icon="🇫🇷",
)

st.image('./img/banner_midjourney.png')

st.title("4C: Control credit card consumption 🇫🇷")

st.write("This application leverages granular card payments data to provide interactive data visualisation. It also provides alerts to detect sudden changes in consumer spending for a wide range of sectors.")

add_logos()

st.markdown(
"""
### Authors
- Hafid Chakir (Cartes Bancaires)
- Florian Le Goff (Insee)
- Lucas Malherbe (Insee)
"""
)

st.image('https://imgtr.ee/images/2023/03/01/RiaxF.jpg', width = 370)

st.markdown(
"""
### Source code

[Github repository](https://github.com/InseeFrLab/hackathon-ntts-2023)

""")