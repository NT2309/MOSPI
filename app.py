import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page configuration
st.set_page_config(
    page_title="MoSPI Project Monitoring Portal",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("MoSPI Project Monitoring Portal")
st.write("Integrated Project Monitoring Dashboard")

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Overview", "Risk & Alerts", "Analytics"]
)


# =========================================================
# LOAD PROJECT DATA
# =========================================================

if os.path.exists("projects.csv"):
    df = pd.read_csv("projects.csv")

else:
    # Temporary fake data until Team 3 provides projects.csv
    data = {
        "Project": [
            "Smart City Development",
            "AI Classroom",
            "Waste Management System",
            "Healthcare Tracker",
            "Smart Traffic Control"
        ],
        "Budget": [
            500000,
            300000,
            450000,
            250000,
            600000
        ],
        "Risk": [
            "Low",
            "High",
            "Medium",
            "Low",
            "High"
        ]
    }

    df = pd.DataFrame(data)


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.header("Project Overview")

    # Metrics
    total_projects = len(df)
    total_budget = df["Budget"].sum()
    high_risk_projects = len(
        df[df["Risk"].astype(str).str.lower() == "high"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Projects",
            total_projects
        )

    with col2:
        st.metric(
            "Total Budget (₹)",
            f"₹{total_budget:,.0f}"
        )

    with col3:
        st.metric(
            "High Risk Projects",
            high_risk_projects
        )

    st.divider()

    # Raw project table
    st.subheader("📋 Project Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# RISK & ALERTS
# =========================================================

elif page == "Risk & Alerts":

    st.header("Risk & Alerts")

    st.info("Risk and alert information will be added here.")


# =========================================================
# ANALYTICS
# =========================================================

elif page == "Analytics":

    st.header("Analytics")

    st.info("Charts and analytics will be added here.")