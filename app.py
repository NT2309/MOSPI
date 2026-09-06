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
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    """
    <style>
        .main-title {
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .subtitle {
            color: #888;
            font-size: 15px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 28px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD CSV
# =========================================================
CSV_FILE = "punjab_haryana_projects(1).csv"
LEGACY_CSV_FILE = "punjab_haryana_projects.csv"

APP_DIR = os.path.dirname(os.path.abspath(__file__))

candidate_files = [
    os.path.join(APP_DIR, CSV_FILE),
    os.path.join(APP_DIR, LEGACY_CSV_FILE),
    os.path.join(os.path.expanduser("~"), "Downloads", CSV_FILE),
    os.path.join(os.path.expanduser("~"), "Downloads", LEGACY_CSV_FILE),
]

found_csv = next((path for path in candidate_files if os.path.isfile(path)), None)

if found_csv is None:
    st.error(
        "CSV file nahi mili. App ke same folder mein "
        f'"{CSV_FILE}" ya "{LEGACY_CSV_FILE}" rakho.'
    )
    st.stop()

CSV_FILE = found_csv


try:
    df = pd.read_csv(CSV_FILE)
except Exception as e:
    st.error(f"CSV load nahi ho paayi: {e}")
    st.stop()


# =========================================================
# REQUIRED COLUMNS CHECK
# =========================================================
required_columns = [
    "Project_ID",
    "Project_Name",
    "State",
    "Lat",
    "Lon",
    "Budget_Crores",
    "Time_Elapsed_Percent",
    "Funds_Spent_Percent",
    "Physical_Progress_Percent"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "CSV mein ye columns missing hain: "
        + ", ".join(missing_columns)
    )
    st.stop()


# =========================================================
# CONVERT NUMERIC COLUMNS
# =========================================================
numeric_columns = [
    "Lat",
    "Lon",
    "Budget_Crores",
    "Time_Elapsed_Percent",
    "Funds_Spent_Percent",
    "Physical_Progress_Percent"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# =========================================================
# RISK CALCULATION
# =========================================================
def calculate_risk(row):

    time_elapsed = row["Time_Elapsed_Percent"]
    physical_progress = row["Physical_Progress_Percent"]
    funds_spent = row["Funds_Spent_Percent"]

    if pd.isna(time_elapsed):
        time_elapsed = 0

    if pd.isna(physical_progress):
        physical_progress = 0

    if pd.isna(funds_spent):
        funds_spent = 0

    score = 0

    # Time vs physical progress
    time_gap = time_elapsed - physical_progress

    if time_gap >= 30:
        score += 50

    elif time_gap >= 15:
        score += 30

    elif time_gap >= 5:
        score += 15

    # Funds spent vs physical progress
    spending_gap = funds_spent - physical_progress

    if spending_gap >= 25:
        score += 30

    elif spending_gap >= 10:
        score += 15

    # Low physical progress
    if physical_progress < 30:
        score += 20

    score = min(score, 100)

    if score >= 60:
        level = "Critical"

    elif score >= 35:
        level = "High"

    elif score >= 15:
        level = "Medium"

    else:
        level = "Low"

    return score, level


risk_results = df.apply(
    calculate_risk,
    axis=1
)

df["Risk_Score"] = [
    result[0] for result in risk_results
]

df["Risk_Level"] = [
    result[1] for result in risk_results
]


# =========================================================
# HEADER
# =========================================================
header1, header2, header3 = st.columns(
    [5, 1, 1]
)

with header1:

    st.markdown(
        '<div class="main-title">'
        '🏗️ MoSPI PAIMANA Portal'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Integrated Project Monitoring & Analytics Platform'
        '</div>',
        unsafe_allow_html=True
    )


with header2:

    with st.popover("🎧 Support"):

        st.markdown("### 📞 Technical Helpdesk")

        st.write(
            "For dashboard assistance or reporting discrepancies:"
        )

        st.write("📧 support-paimana@mospi.gov.in")
        st.write("📞 1800-11-2026")

        st.caption(
            "Mon–Fri | 9:00 AM – 5:30 PM IST"
        )


with header3:

    role = st.selectbox(
        "User Type",
        [
            "Government Official",
            "Citizen"
        ]
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

st.sidebar.metric(
    "Projects Loaded",
    len(df)
)

st.sidebar.caption(
    "Data Source: PAIMANA Project Dataset"
)


# =========================================================
# PROJECT DETAILS
# =========================================================
def show_project_details(row):

    st.markdown("### 📋 Project Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Project ID:** {row['Project_ID']}"
        )

        st.write(
            f"**Project:** {row['Project_Name']}"
        )

        st.write(
            f"**State:** {row['State']}"
        )

        st.write(
            f"**Budget:** ₹{row['Budget_Crores']:,.2f} Cr"
        )

    with col2:

        st.write(
            f"**Time Elapsed:** "
            f"{row['Time_Elapsed_Percent']:.1f}%"
        )

        st.write(
            f"**Funds Spent:** "
            f"{row['Funds_Spent_Percent']:.1f}%"
        )

        st.write(
            f"**Physical Progress:** "
            f"{row['Physical_Progress_Percent']:.1f}%"
        )

        st.write(
            f"**Risk:** "
            f"{row['Risk_Level']} "
            f"({row['Risk_Score']}/100)"
        )

    st.write("#### Physical Progress")

    progress_value = int(
        min(
            max(
                row["Physical_Progress_Percent"],
                0
            ),
            100
        )
    )

    st.progress(progress_value)

    time_gap = (
        row["Time_Elapsed_Percent"]
        - row["Physical_Progress_Percent"]
    )

    if time_gap >= 30:

        st.error(
            f"🚨 Critical Warning: "
            f"Physical progress is {time_gap:.1f}% "
            f"behind the elapsed timeline."
        )

    elif time_gap >= 15:

        st.warning(
            f"⚠️ Warning: "
            f"Physical progress is {time_gap:.1f}% "
            f"behind the elapsed timeline."
        )

    else:

        st.success(
            "🟢 Project progress is currently "
            "within the monitoring threshold."
        )


# =========================================================
# OVERVIEW
# =========================================================
if page == "Overview":

    st.header("📊 Project Overview")

    total_projects = len(df)

    total_budget = df[
        "Budget_Crores"
    ].sum()

    average_progress = df[
        "Physical_Progress_Percent"
    ].mean()

    high_risk_projects = len(
        df[
            df["Risk_Level"].isin(
                ["High", "Critical"]
            )
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Projects",
            f"{total_projects:,}"
        )

    with col2:

        st.metric(
            "Total Budget",
            f"₹{total_budget:,.0f} Cr"
        )

    with col3:

        st.metric(
            "Avg Physical Progress",
            f"{average_progress:.1f}%"
        )

    with col4:

        st.metric(
            "High / Critical Risk",
            f"{high_risk_projects:,}"
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
            Avg_Progress=(
                "Physical_Progress_Percent",
                "mean"
            ),
            Avg_Funds_Spent=(
                "Funds_Spent_Percent",
                "mean"
            )
        )
        .reset_index()
    )

    state_summary["Budget_Cr"] = (
        state_summary["Budget_Cr"].round(2)
    )

    state_summary["Avg_Progress"] = (
        state_summary["Avg_Progress"].round(1)
    )

    state_summary["Avg_Funds_Spent"] = (
        state_summary["Avg_Funds_Spent"].round(1)
    )

    display_summary = state_summary.rename(
        columns={
            "State": "State",
            "Projects": "Projects",
            "Budget_Cr": "Budget (₹ Cr)",
            "Avg_Progress": "Avg Progress (%)",
            "Avg_Funds_Spent": "Avg Funds Spent (%)"
        }
    )

    # Non-clickable table
    st.table(display_summary)

    # -----------------------------------------------------
    # PROJECT COUNT CHART
    # -----------------------------------------------------
    state_summary["Projects"] = pd.to_numeric(
        state_summary["Projects"], errors="coerce"
    ).fillna(0).astype(int)

    max_projects = int(state_summary["Projects"].max()) if not state_summary.empty else 0
    y_max = max(5, max_projects + 5)

    fig = px.bar(
        state_summary,
        x="State",
        y="Projects",
        text="Projects",
        title="Projects by State",
        range_y=[0, y_max]
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Number of Projects",
        height=420,
        margin=dict(t=70, b=50, l=50, r=30),
        yaxis=dict(
            range=[0, y_max],
            dtick=5 if y_max <= 50 else None
        )
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

    states = sorted(
        df["State"]
        .dropna()
        .unique()
        .tolist()
    )

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
    # METRICS
    # -----------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Projects",
            f"{len(state_df):,}"
        )

    with col2:

        budget_value = state_df[
            "Budget_Crores"
        ].sum()

        st.metric(
            "Budget",
            f"₹{budget_value:,.0f} Cr"
        )

    with col3:

        progress_value = state_df[
            "Physical_Progress_Percent"
        ].mean()

        st.metric(
            "Physical Progress",
            f"{progress_value:.1f}%"
        )

    with col4:

        funds_value = state_df[
            "Funds_Spent_Percent"
        ].mean()

        st.metric(
            "Funds Spent",
            f"{funds_value:.1f}%"
        )

    st.divider()

    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------
    st.subheader("📍 Project Locations")

    map_df = state_df.dropna(
        subset=["Lat", "Lon"]
    )

    if not map_df.empty:

        fig_map = px.scatter_map(
            map_df,
            lat="Lat",
            lon="Lon",
            hover_name="Project_Name",
            hover_data={
                "Project_ID": True,
                "State": True,
                "Budget_Crores": ":.2f",
                "Physical_Progress_Percent": ":.1f",
                "Risk_Level": True,
                "Lat": False,
                "Lon": False
            },
            color="Risk_Level",
            zoom=5,
            height=520
        )

        fig_map.update_layout(
            map_style="open-street-map",
            margin={
                "r": 0,
                "t": 0,
                "l": 0,
                "b": 0
            }
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True
        )

    else:

        st.info(
            "No geographical coordinates available."
        )

    # -----------------------------------------------------
    # PROJECT CARDS
    # -----------------------------------------------------
    st.subheader("📋 Projects")

    for index, row in state_df.reset_index(
        drop=True
    ).iterrows():

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [4, 2, 2, 1]
            )

            with col1:

                st.markdown(
                    f"**{row['Project_Name']}**"
                )

                st.caption(
                    f"{row['Project_ID']} • "
                    f"{row['State']}"
                )

            with col2:

                st.write(
                    f"Progress: "
                    f"**{row['Physical_Progress_Percent']:.1f}%**"
                )

            with col3:

                st.write(
                    f"Risk: **{row['Risk_Level']}**"
                )

                st.caption(
                    f"Score: {row['Risk_Score']}/100"
                )

            with col4:

                details_key = (
                    "state_details_"
                    + str(row["Project_ID"])
                    + "_"
                    + str(index)
                )

                if st.button(
                    "Details",
                    key=details_key
                ):

                    st.session_state[
                        "selected_project_id"
                    ] = row["Project_ID"]

            # Show details directly on page
            if (
                st.session_state.get(
                    "selected_project_id"
                )
                == row["Project_ID"]
            ):

                show_project_details(row)


# =========================================================
# RISK & ALERTS
# =========================================================
elif page == "Risk & Alerts":

    st.header("🚨 Risk & Early Warning Centre")

    st.write(
        "Automated monitoring engine identifies "
        "projects requiring early intervention."
    )

    risk_counts = (
        df["Risk_Level"]
        .value_counts()
        .reindex(
            [
                "Critical",
                "High",
                "Medium",
                "Low"
            ],
            fill_value=0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🚨 Critical",
            int(risk_counts["Critical"])
        )

    with col2:

        st.metric(
            "🔴 High",
            int(risk_counts["High"])
        )

    with col3:

        st.metric(
            "🟡 Medium",
            int(risk_counts["Medium"])
        )

    with col4:

        st.metric(
            "🟢 Low",
            int(risk_counts["Low"])
        )

    st.divider()

    alert_df = df[
        df["Risk_Level"].isin(
            ["Critical", "High"]
        )
    ].sort_values(
        "Risk_Score",
        ascending=False
    )

    st.subheader(
        "⚠️ Projects Requiring Attention"
    )

    if alert_df.empty:

        st.success(
            "🟢 No high-risk projects detected."
        )

    else:

        for _, row in alert_df.iterrows():

            if row["Risk_Level"] == "Critical":

                st.error(
                    f"🚨 {row['Project_Name']} | "
                    f"{row['State']} | "
                    f"Risk Score: "
                    f"{row['Risk_Score']}/100"
                )

            else:

                st.warning(
                    f"⚠️ {row['Project_Name']} | "
                    f"{row['State']} | "
                    f"Risk Score: "
                    f"{row['Risk_Score']}/100"
                )

            time_gap = (
                row["Time_Elapsed_Percent"]
                - row["Physical_Progress_Percent"]
            )

            spending_gap = (
                row["Funds_Spent_Percent"]
                - row["Physical_Progress_Percent"]
            )

            st.caption(
                f"Time-progress gap: "
                f"{time_gap:.1f}% | "
                f"Funds-progress gap: "
                f"{spending_gap:.1f}%"
            )


# =========================================================
# ANALYTICS
# =========================================================
elif page == "Analytics":

    st.header("📈 Comparative Analytics")

    # -----------------------------------------------------
    # TIME VS PROGRESS
    # -----------------------------------------------------
    st.subheader(
        "⏱️ Time Elapsed vs Physical Progress"
    )

    fig1 = px.scatter(
        df,
        x="Time_Elapsed_Percent",
        y="Physical_Progress_Percent",
        size="Budget_Crores",
        color="Risk_Level",
        hover_name="Project_Name",
        hover_data=[
            "Project_ID",
            "State"
        ],
        title="Project Progress Performance"
    )

    fig1.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=100,
        y1=100,
        line=dict(
            dash="dash"
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.info(
        "Projects below the diagonal line are "
        "progressing slower than their elapsed timeline."
    )

    # -----------------------------------------------------
    # FUNDS VS PROGRESS
    # -----------------------------------------------------
    st.subheader(
        "💰 Funds Spent vs Physical Progress"
    )

    fig2 = px.scatter(
        df,
        x="Funds_Spent_Percent",
        y="Physical_Progress_Percent",
        size="Budget_Crores",
        color="State",
        hover_name="Project_Name",
        hover_data=[
            "Project_ID"
        ],
        title="Financial vs Physical Progress"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # -----------------------------------------------------
    # STATE COMPARISON
    # -----------------------------------------------------
    st.subheader(
        "🏛️ State-wise Performance"
    )

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
        "Search by Project Name, Project ID or State",
        placeholder="e.g. Punjab / Haryana / P001"
    )

    filtered_df = df.copy()

    if search.strip():

        search_text = search.strip().lower()

        filtered_df = filtered_df[
            filtered_df["Project_Name"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
            |
            filtered_df["Project_ID"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
            |
            filtered_df["State"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        ]

    st.write(
        f"Found **{len(filtered_df)}** project(s)"
    )

    if filtered_df.empty:

        st.warning(
            "No matching projects found."
        )

    else:

        for index, row in filtered_df.reset_index(
            drop=True
        ).iterrows():

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [4, 2, 2, 1]
                )

                with col1:

                    st.markdown(
                        f"**{row['Project_Name']}**"
                    )

                    st.caption(
                        f"{row['Project_ID']} • "
                        f"{row['State']}"
                    )

                with col2:

                    st.write(
                        "Progress"
                    )

                    st.write(
                        f"**{row['Physical_Progress_Percent']:.1f}%**"
                    )

                with col3:

                    st.write(
                        "Risk"
                    )

                    st.write(
                        f"**{row['Risk_Level']}**"
                    )

                with col4:

                    search_key = (
                        "search_details_"
                        + str(row["Project_ID"])
                        + "_"
                        + str(index)
                    )

                    if st.button(
                        "Details",
                        key=search_key
                    ):

                        st.session_state[
                            "search_selected_project"
                        ] = row["Project_ID"]

            if (
                st.session_state.get(
                    "search_selected_project"
                )
                == row["Project_ID"]
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