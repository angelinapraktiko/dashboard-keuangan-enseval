
from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    file_path = (
        Path(__file__).parent
        / "data"
        / "dataset_project_magang_bersih.csv"
    )

    df = pd.read_csv(file_path)

    return df
