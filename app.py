import os
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="MoSPI PAIMANA Portal",
    page_icon="🏗️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #666;
        font-size: 15px;
    }

    .alert-box {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD CSV
# =========================================================
CSV_FILE = "punjab_haryana_projects.csv"

if not os.path.exists(CSV_FILE):

    # Also check Downloads folder for local testing
    downloads_file = os.path.join(
        os.path.expanduser("~"),
        "Downloads",
        CSV_FILE
    )

    if os.path.exists(downloads_file):
        CSV_FILE = downloads_file
    else:
        st.error(
            f"❌ `{CSV_FILE}` nahi mila. "
            "CSV ko app.py ke same folder mein rakho."
        )
        st.stop()

df = pd.read_csv(CSV_FILE)

# =========================================================
# CLEAN DATA
# =========================================================
numeric_columns = [
    "Budget_Crores",
    "Time_Elapsed_Percent",
    "Funds_Spent_Percent",
    "Physical_Progress_Percent",
    "Lat",
    "Lon"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================================================
# AUTOMATIC RISK ENGINE
# =========================================================
def calculate_risk(row):

    time = row["Time_Elapsed_Percent"]
    progress = row["Physical_Progress_Percent"]
    funds = row["Funds_Spent_Percent"]

    risk_score = 0

    # Time-progress gap
    if time - progress >= 30:
        risk_score += 50
    elif time - progress >= 15:
        risk_score += 30
    elif time - progress >= 5:
        risk_score += 15

    # Money being spent faster than physical work
    if funds - progress >= 25:
        risk_score += 30
    elif funds - progress >= 10:
        risk_score += 15

    # Very low progress
    if progress < 30:
        risk_score += 20

    if risk_score >= 60:
        return risk_score, "Critical"
    elif risk_score >= 35:
        return risk_score, "High"
    elif risk_score >= 15:
        return risk_score, "Medium"
    else:
        return risk_score, "Low"


risk_results = df.apply(calculate_risk, axis=1)

df["Risk_Score"] = [x[0] for x in risk_results]
df["Risk_Level"] = [x[1] for x in risk_results]

# =========================================================
# HEADER
# =========================================================
header_col1, header_col2, header_col3 = st.columns([5, 1, 1])

with header_col1:
    st.markdown(
        '<div class="main-title">🏗️ MoSPI PAIMANA Portal</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Integrated Project Monitoring & Analytics Platform'
        '</div>',
        unsafe_allow_html=True
    )

with header_col2:
    st.write("")

    with st.popover("🎧 Support"):
        st.markdown("### 📞 Technical Helpdesk")
        st.write("For dashboard assistance:")
        st.write("📧 support-paimana@mospi.gov.in")
        st.write("📞 1800-11-2026")
        st.caption("Mon–Fri | 9:00 AM – 5:30 PM IST")

with header_col3:
    st.write("")

    role = st.selectbox(
        "User Type",
        ["Government Official", "Citizen"]
    )

st.divider()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "State-wise Monitoring",
        "Risk & Alerts",
        "Analytics",
        "Project Search"
    ]
)

st.sidebar.divider()

st.sidebar.caption("📊 Data Source")
st.sidebar.write("PAIMANA Project Database")

st.sidebar.caption(
    f"Projects loaded: {len(df)}"
)

# =========================================================
# PROJECT DETAILS DIALOG
# =========================================================
@st.dialog("📋 Project Details")
def show_project_details(row):

    st.subheader(row["Project_Name"])

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Project ID:** {row['Project_ID']}")
        st.write(f"**State:** {row['State']}")
        st.write(f"**Budget:** ₹{row['Budget_Crores']} Crore")
        st.write(
            f"**Physical Progress:** "
            f"{row['Physical_Progress_Percent']}%"
        )

    with col2:
        st.write(
            f"**Time Elapsed:** "
            f"{row['Time_Elapsed_Percent']}%"
        )

        st.write(
            f"**Funds Spent:** "
            f"{row['Funds_Spent_Percent']}%"
        )

        st.write(
            f"**Risk Score:** "
            f"{row['Risk_Score']}"
        )

        st.write(
            f"**Risk Level:** "
            f"{row['Risk_Level']}"
        )

    st.divider()

    progress = row["Physical_Progress_Percent"]

    st.write("### Project Progress")

    st.progress(
        min(max(int(progress), 0), 100)
    )

    # Early warning
    if row["Risk_Level"] == "Critical":
        st.error(
            "🚨 CRITICAL: Project requires immediate monitoring."
        )
    elif row["Risk_Level"] == "High":
        st.warning(
            "⚠️ HIGH RISK: Early intervention recommended."
        )
    elif row["Risk_Level"] == "Medium":
        st.info(
            "🟡 MEDIUM RISK: Continue close monitoring."
        )
    else:
        st.success(
            "🟢 LOW RISK: Project currently progressing normally."
        )

# =========================================================
# OVERVIEW
# =========================================================
if page == "Overview":

    st.header("📊 Project Overview")

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    total_projects = len(df)
    total_budget = df["Budget_Crores"].sum()
    avg_progress = df["Physical_Progress_Percent"].mean()

    high_risk = len(
        df[df["Risk_Level"].isin(["High", "Critical"])]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Projects",
            total_projects
        )

    with c2:
        st.metric(
            "Total Budget",
            f"₹{total_budget:,.2f} Cr"
        )

    with c3:
        st.metric(
            "Avg Physical Progress",
            f"{avg_progress:.1f}%"
        )

    with c4:
        st.metric(
            "High/Critical Risk",
            high_risk
        )

    st.divider()

    # -----------------------------------------------------
    # STATE SUMMARY
    # -----------------------------------------------------

    st.subheader("🇮🇳 State-wise Project Summary")

    state_summary = (
        df.groupby("State")
        .agg(
            Projects=("Project_ID", "count"),
            Budget_Cr=("Budget_Crores", "sum"),
            Avg_Progress=("Physical_Progress_Percent", "mean"),
            Avg_Funds_Spent=("Funds_Spent_Percent", "mean")
        )
        .reset_index()
    )

    state_summary["Avg_Progress"] = (
        state_summary["Avg_Progress"].round(1)
    )

    state_summary["Avg_Funds_Spent"] = (
        state_summary["Avg_Funds_Spent"].round(1)
    )

    st.dataframe(
        state_summary,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # STATE CHART
    # -----------------------------------------------------

    fig = px.bar(
        state_summary,
        x="State",
        y="Projects",
        title="Projects by State",
        text="Projects"
    )

    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Number of Projects"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# STATE-WISE MONITORING
# =========================================================
elif page == "State-wise Monitoring":

    st.header("🗺️ State-wise Project Monitoring")

    states = sorted(df["State"].dropna().unique())

    selected_state = st.selectbox(
        "Select State",
        ["All States"] + states
    )

    if selected_state == "All States":
        state_df = df.copy()
    else:
        state_df = df[
            df["State"] == selected_state
        ].copy()

    # -----------------------------------------------------
    # STATE METRICS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Projects",
            len(state_df)
        )

    with c2:
        st.metric(
            "Budget",
            f"₹{state_df['Budget_Crores'].sum():,.2f} Cr"
        )

    with c3:
        st.metric(
            "Physical Progress",
            f"{state_df['Physical_Progress_Percent'].mean():.1f}%"
        )

    with c4:
        st.metric(
            "Funds Spent",
            f"{state_df['Funds_Spent_Percent'].mean():.1f}%"
        )

    st.divider()

    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    st.subheader("📍 Project Locations")

    map_df = state_df.dropna(
        subset=["Lat", "Lon"]
    )

    if len(map_df) > 0:

        fig_map = px.scatter_map(
            map_df,
            lat="Lat",
            lon="Lon",
            hover_name="Project_Name",
            hover_data=[
                "Project_ID",
                "State",
                "Budget_Crores",
                "Physical_Progress_Percent",
                "Risk_Level"
            ],
            color="Risk_Level",
            zoom=4,
            height=500
        )

        fig_map.update_layout(
            map_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True
        )

    # -----------------------------------------------------
    # PROJECT TABLE
    # -----------------------------------------------------

    st.subheader("📋 Projects")

    display_columns = [
        "Project_ID",
        "Project_Name",
        "State",
        "Budget_Crores",
        "Time_Elapsed_Percent",
        "Funds_Spent_Percent",
        "Physical_Progress_Percent",
        "Risk_Score",
        "Risk_Level"
    ]

    st.dataframe(
        state_df[display_columns],
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# RISK & ALERTS
# =========================================================
elif page == "Risk & Alerts":

    st.header("🚨 Risk & Early Warning Centre")

    st.write(
        "AI-ready rule-based risk engine identifies projects "
        "requiring early intervention."
    )

    # -----------------------------------------------------
    # RISK COUNTS
    # -----------------------------------------------------

    risk_counts = (
        df["Risk_Level"]
        .value_counts()
        .reindex(
            ["Critical", "High", "Medium", "Low"],
            fill_value=0
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🚨 Critical",
            risk_counts["Critical"]
        )

    with c2:
        st.metric(
            "🔴 High",
            risk_counts["High"]
        )

    with c3:
        st.metric(
            "🟡 Medium",
            risk_counts["Medium"]
        )

    with c4:
        st.metric(
            "🟢 Low",
            risk_counts["Low"]
        )

    st.divider()

    # -----------------------------------------------------
    # ALERTS
    # -----------------------------------------------------

    critical_df = df[
        df["Risk_Level"].isin(["Critical", "High"])
    ].sort_values(
        "Risk_Score",
        ascending=False
    )

    st.subheader("⚠️ Projects Requiring Attention")

    if len(critical_df) == 0:

        st.success(
            "No high-risk projects detected."
        )

    else:

        for _, row in critical_df.iterrows():

            if row["Risk_Level"] == "Critical":

                st.error(
                    f"🚨 **{row['Project_Name']}** | "
                    f"{row['State']} | "
                    f"Risk Score: {row['Risk_Score']}"
                )

            else:

                st.warning(
                    f"⚠️ **{row['Project_Name']}** | "
                    f"{row['State']} | "
                    f"Risk Score: {row['Risk_Score']}"
                )

            with st.expander("View warning details"):

                st.write(
                    f"**Time elapsed:** "
                    f"{row['Time_Elapsed_Percent']}%"
                )

                st.write(
                    f"**Physical progress:** "
                    f"{row['Physical_Progress_Percent']}%"
                )

                st.write(
                    f"**Funds spent:** "
                    f"{row['Funds_Spent_Percent']}%"
                )

                gap = (
                    row["Time_Elapsed_Percent"]
                    - row["Physical_Progress_Percent"]
                )

                st.write(
                    f"**Time vs Progress Gap:** "
                    f"{gap:.1f}%"
                )

# =========================================================
# ANALYTICS
# =========================================================
elif page == "Analytics":

    st.header("📈 Comparative Analytics")

    # -----------------------------------------------------
    # CHART 1
    # -----------------------------------------------------

    st.subheader("⏱️ Time Elapsed vs Physical Progress")

    fig1 = px.scatter(
        df,
        x="Time_Elapsed_Percent",
        y="Physical_Progress_Percent",
        size="Budget_Crores",
        color="Risk_Level",
        hover_name="Project_Name",
        hover_data=["State", "Project_ID"],
        title="Project Progress Performance"
    )

    fig1.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=100,
        y1=100,
        line=dict(dash="dash")
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.info(
        "Projects below the diagonal line have physical progress "
        "behind the elapsed project timeline."
    )

    # -----------------------------------------------------
    # CHART 2
    # -----------------------------------------------------

    st.subheader("💰 Funds Spent vs Physical Progress")

    fig2 = px.scatter(
        df,
        x="Funds_Spent_Percent",
        y="Physical_Progress_Percent",
        size="Budget_Crores",
        color="State",
        hover_name="Project_Name",
        title="Financial vs Physical Progress"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # -----------------------------------------------------
    # CHART 3
    # -----------------------------------------------------

    st.subheader("🏗️ State-wise Performance")

    performance = (
        df.groupby("State")
        .agg(
            Physical_Progress=(
                "Physical_Progress_Percent",
                "mean"
            ),
            Funds_Spent=(
                "Funds_Spent_Percent",
                "mean"
            )
        )
        .reset_index()
    )

    fig3 = px.bar(
        performance,
        x="State",
        y=[
            "Physical_Progress",
            "Funds_Spent"
        ],
        barmode="group",
        title="State-wise Physical Progress vs Funds Spent"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =========================================================
# PROJECT SEARCH
# =========================================================
elif page == "Project Search":

    st.header("🔎 Project Search")

    search = st.text_input(
        "Search Project Name / Project ID / State"
    )

    filtered = df.copy()

    if search:

        search_lower = search.lower()

        filtered = filtered[
            filtered["Project_Name"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower)
            |
            filtered["Project_ID"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower)
            |
            filtered["State"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower)
        ]

    st.write(
        f"Found **{len(filtered)}** project(s)"
    )

    # -----------------------------------------------------
    # PROJECT CARDS
    # -----------------------------------------------------

    for index, row in filtered.iterrows():

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(
                [4, 2, 2, 1]
            )

            with c1:
                st.markdown(
                    f"### {row['Project_Name']}"
                )
                st.caption(
                    f"{row['Project_ID']} • {row['State']}"
                )

            with c2:
                st.write(
                    f"**Progress**\n\n"
                    f"{row['Physical_Progress_Percent']}%"
                )

            with c3:
                st.write(
                    f"**Risk**\n\n"
                    f"{row['Risk_Level']}"
                )

            with c4:
                if st.button(
                    "Details",
                    key=f"search_{index}"
                ):
                    show_project_details(row)

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "MoSPI PAIMANA Portal | SIH Prototype | "
    "Project Monitoring & Early Warning System"
)