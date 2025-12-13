"""
Streamlit App: Staffing Optimization Engine

Demo-optimized version:
- Locked to bundled dataset (no file uploads)
- Hourly staffing optimization
- Cost minimization under demand coverage constraints
- Designed for fast, reliable Streamlit deployment

Purpose: Demonstrate prescriptive analytics for workforce planning.
"""

import streamlit as st
import pandas as pd
import numpy as np

from optimizer_scipy import optimize_staffing

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Staffing Optimization Engine",
    page_icon="🧑‍💼",
    layout="wide"
)

# --------------------------------------------------
# APP HEADER
# --------------------------------------------------
st.title("🧑‍💼 Staffing Optimization Engine")
st.markdown(
    """
    **Prescriptive Analytics Demo**

    This application demonstrates how optimization can be used to generate
    **cost-optimal hourly staffing plans** based on historical demand.
    The model guarantees demand coverage while minimizing total labor cost.
    """
)

# --------------------------------------------------
# DATA SOURCE (LOCKED)
# --------------------------------------------------
DATA_PATH = "data/cafe_hourly_demand_3months.csv"

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = pd.to_numeric(df["hour"])
    df["time_bucket"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")
    return df.sort_values("time_bucket").reset_index(drop=True)

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Dataset not found at `{DATA_PATH}`. "
        "Ensure the file exists in the GitHub repository."
    )
    st.stop()

st.info(f"Using bundled staffing dataset ({len(df):,} hourly records)")

# --------------------------------------------------
# SIDEBAR ASSUMPTIONS
# --------------------------------------------------
st.sidebar.header("⚙️ Model Assumptions")

productivity = st.sidebar.number_input(
    "Customers per staff per hour",
    min_value=1.0,
    value=8.0,
    step=1.0,
    help="Operational productivity assumption"
)

service_buffer = st.sidebar.slider(
    "Service buffer",
    min_value=_
