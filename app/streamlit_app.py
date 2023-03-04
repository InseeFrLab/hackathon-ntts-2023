import streamlit as st
from streamlit_utils import add_logos

st.set_page_config(
    page_title="NTTS Hackathon - Dashboard of the winning team",
    page_icon=":flag-mf:",
)

st.title("NTTS Hackathon - Dashboard of the winning team :flag-mf:")

st.write("Welcome to our world !")

add_logos()

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This dashboard is so going to win it all.
    """
)
