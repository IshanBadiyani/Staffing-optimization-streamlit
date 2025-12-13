import streamlit as st
import pandas as pd
import numpy as np
from optimizer_scipy import optimize_staffing

st.set_page_config(
    page_title="Staffing Optimization Engine",
    layout="wide"
)

st.title("Staffing Optimization Engine")
st.caption("Prescriptive analytics for cost-optimal hourly staffing")

uploaded_file = st.file_uploader(
    "Upload demand CSV",
    type=["csv"]
)

with st.sidebar:
    st.header("Model Assumptions")
    productivity = st.number_input(
        "Customers per staff per hour",
        min_value=1.0,
        value=8.0,
        step=1.0
    )
    buffer = st.slider(
        "Service buffer",
        min_value=1.0,
        max_value=1.5,
        value=1.0,
        step=0.05
    )
    max_staff = st.number_input(
        "Max staff per hour (optional)",
        min_value=0,
        value=0,
        step=1
    )
    overstaff_penalty = st.number_input(
        "Overstaffing penalty",
        min_value=0.0,
        value=0.0,
        step=0.5
    )

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = {"date", "hour", "demand", "hourly_wage"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain columns: {required_cols}")
        st.stop()

    # Build datetime bucket
    df["date"] = pd.to_datetime(df["date"])
    df["time_bucket"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")
    df = df.sort_values("time_bucket")

    # Required staff
    df["required_staff"] = np.ceil(
        (df["demand"] / productivity) * buffer
    ).astype(int)

    # Optimize
    staff_plan, total_cost = optimize_staffing(
        required_staff=df["required_staff"].values,
        hourly_wage=df["hourly_wage"].values,
        max_staff=None if max_staff == 0 else int(max_staff),
        overstaff_penalty=overstaff_penalty
    )

    df["planned_staff"] = staff_plan
    df["gap"] = df["planned_staff"] - df["required_staff"]
    df["hourly_cost"] = df["planned_staff"] * df["hourly_wage"]

    st.subheader("Staffing Plan Summary")
    st.metric("Total Labor Cost", f"${total_cost:,.2f}")

    st.subheader("Demand vs Staffing")
    st.line_chart(
        df.set_index("time_bucket")[[
            "demand",
            "required_staff",
            "planned_staff"
        ]]
    )

    st.subheader("Detailed Output")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download staffing_plan_output.csv",
        data=csv,
        file_name="staffing_plan_output.csv",
        mime="text/csv"
    )
else:
    st.info("Upload a CSV file to begin optimization.")
