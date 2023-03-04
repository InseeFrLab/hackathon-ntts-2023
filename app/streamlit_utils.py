"""
Streamlit utils.
"""
import os
import streamlit as st
import s3fs
import pandas as pd


def get_file_system():
    """
    Return s3 file system.
    """
    return s3fs.S3FileSystem(
        client_kwargs={
            "endpoint_url": "https://" + os.environ["AWS_S3_ENDPOINT"]
        },
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    )


def add_logos():
    """
    Add logos on top of sidebar.
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://imgtr.ee/images/2023/03/01/RiaxF.jpg);
                background-repeat: no-repeat;
                margin-left: 10px;
                margin-right: 10px;
                margin-top: 50px;
                padding-top: 120px;
                background-size: contain;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


@st.cache_data(ttl=600)
def read_csv(filename):
    """
    Read csv from Minio.
    """
    fs = get_file_system()
    with fs.open(filename, 'r') as f:
        return pd.read_csv(f)


@st.cache_data(ttl=600)
def read_html(filename):
    """
    Read html from Minio.
    """
    fs = get_file_system()
    with fs.open(filename, 'r') as f:
        return f.read()
