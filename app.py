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
    min_value=1.0,
    max_value=1.5,
    value=1.0,
    step=0.05,
    help="Extra staffing buffer for service reliability"
)

max_staff = st.sidebar.number_input(
    "Max staff per hour (optional)",
    min_value=0,
    value=0,
    step=1,
    help="Physical or managerial capacity constraint"
)

overstaff_penalty = st.sidebar.number_input(
    "Overstaffing penalty ($ per staff-hour)",
    min_value=0.0,
    value=0.0,
    step=0.5,
    help="Soft penalty to discourage unnecessary overstaffing"
)

run_button = st.sidebar.button(
    "🚀 Run Staffing Optimization",
    type="primary"
)

# --------------------------------------------------
# PREPARE DEMAND
# --------------------------------------------------
df["required_staff"] = np.ceil(
    (df["demand"] / productivity) * service_buffer
).astype(int)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
st.subheader("📄 Hourly Demand Snapshot")
st.dataframe(
    df[
        ["time_bucket", "demand", "hourly_wage", "required_staff"]
    ].head(24),
    use_container_width=True
)

# --------------------------------------------------
# RUN OPTIMIZATION
# --------------------------------------------------
if run_button:

    st.markdown("## 🚀 Optimization Results")

    with st.spinner("Solving staffing optimization model..."):

        staff_plan, total_cost = optimize_staffing(
            required_staff=df["required_staff"].values,
            hourly_wage=df["hourly_wage"].values,
            max_staff=None if max_staff == 0 else int(max_staff),
            overstaff_penalty=overstaff_penalty
        )

    df["planned_staff"] = staff_plan
    df["gap"] = df["planned_staff"] - df["required_staff"]
    df["hourly_cost"] = df["planned_staff"] * df["hourly_wage"]

    # --------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------
    st.subheader("📊 Staffing Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Labor Cost", f"${total_cost:,.2f}")
    c2.metric("Avg Staff / Hour", f"{df['planned_staff'].mean():.2f}")
    c3.metric("Peak Staff Required", int(df["planned_staff"].max()))

    # --------------------------------------------------
    # VISUALS
    # --------------------------------------------------
    st.subheader("📈 Demand vs Staffing")

    chart_df = df.set_index("time_bucket")[
        ["required_staff", "planned_staff"]
    ]

    st.line_chart(chart_df, height=400)

    st.subheader("💰 Hourly Labor Cost")
    st.line_chart(
        df.set_index("time_bucket")["hourly_cost"],
        height=300
    )

    # --------------------------------------------------
    # DETAILED OUTPUT
    # --------------------------------------------------
    st.subheader("📋 Detailed Staffing Plan")

    st.dataframe(
        df[
            [
                "time_bucket",
                "demand",
                "hourly_wage",
                "required_staff",
                "planned_staff",
                "gap",
                "hourly_cost"
            ]
        ],
        use_container_width=True
    )

    # --------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download staffing_plan_output.csv",
        data=csv,
        file_name="staffing_plan_output.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Built for ISOM 839 – Prescriptive Analytics | "
    "Staffing Optimization | SciPy | Demo Mode"
)
