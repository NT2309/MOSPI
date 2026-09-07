import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAIMANA - Government Project Monitoring Dashboard
# Data source:
# PAIMANA_July_2026_all_ongoing_projects_final.csv
# ============================================================

st.set_page_config(
    page_title="MoSPI PAIMANA Portal",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        color: #666;
        margin-bottom: 1rem;
    }
    .risk-card {
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data loading
# -----------------------------
REQUIRED_COLUMNS = [
    "Project ID",
    "Project Name",
    "Lattitude",
    "Longitude",
    "Budget",
    "Time Elapsed Percent",
    "Fund Spent Percent",
    "Physical Progress Percent",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(
    BASE_DIR,
    "PAIMANA_July_2026_all_ongoing_projects_final.csv",
)


@st.cache_data
def load_data():
    # The CSV is bundled with the app. This works locally and after deployment.
    if not os.path.isfile(CSV_PATH):
        return None, (
            "Government CSV not found. Put "
            "PAIMANA_July_2026_all_ongoing_projects_final.csv "
            "in the same folder as app.py."
        )

    try:
        data = pd.read_csv(CSV_PATH, low_memory=False)
    except Exception as exc:
        return None, f"Could not read government CSV: {exc}"

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        return None, (
            "The uploaded CSV is missing these required columns: "
            + ", ".join(missing)
        )

    # Convert numeric fields safely.
    numeric_cols = [
        "Project ID",
        "Lattitude",
        "Longitude",
        "Budget",
        "Time Elapsed Percent",
        "Fund Spent Percent",
        "Physical Progress Percent",
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=["Project ID", "Project Name", "Lattitude", "Longitude"]).copy()

    # Keep percentages in a sensible range for the dashboard.
    for col in [
        "Time Elapsed Percent",
        "Fund Spent Percent",
        "Physical Progress Percent",
    ]:
        data[col] = data[col].clip(lower=0, upper=100)

    # Risk calculation:
    # - Physical progress behind time elapsed => schedule risk.
    # - Funds spent much higher than physical progress => financial risk.
    data["Schedule Gap"] = (
        data["Time Elapsed Percent"] - data["Physical Progress Percent"]
    )
    data["Fund Gap"] = (
        data["Fund Spent Percent"] - data["Physical Progress Percent"]
    )

    def risk_score(row):
        score = 0

        schedule_gap = row["Schedule Gap"]
        fund_gap = row["Fund Gap"]

        if pd.notna(schedule_gap):
            if schedule_gap >= 30:
                score += 2
            elif schedule_gap >= 15:
                score += 1

        if pd.notna(fund_gap):
            if fund_gap >= 30:
                score += 2
            elif fund_gap >= 15:
                score += 1

        return score

    data["Risk_Score"] = data.apply(risk_score, axis=1)

    def risk_level(score):
        if score >= 3:
            return "High"
        if score >= 1:
            return "Medium"
        return "Low"

    data["Risk_Level"] = data["Risk_Score"].apply(risk_level)

    # The government CSV does not contain a State column.
    # We intentionally do NOT invent state names from coordinates.
    data["Location"] = (
        data["Lattitude"].round(4).astype(str)
        + ", "
        + data["Longitude"].round(4).astype(str)
    )

    return data, None


df, load_error = load_data()

if df is None:
    st.error(
        "CSV file could not be loaded. Put "
        "`PAIMANA_July_2026_all_ongoing_projects_final.csv` "
        "in the same folder as this app.py."
    )
    if load_error:
        st.error(load_error)
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🏗️ MoSPI PAIMANA Portal</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Government Project Monitoring & Analytics Dashboard</div>',
    unsafe_allow_html=True,
)

header_col1, header_col2 = st.columns([5, 1])

with header_col1:
    st.caption(
        f"Official dataset loaded: {len(df):,} ongoing project records"
    )

with header_col2:
    language = st.selectbox(
        "Language",
        ["English", "हिन्दी", "ਪੰਜਾਬੀ"],
        label_visibility="collapsed",
    )

# -----------------------------
# Language helper
# -----------------------------
translations = {
    "English": {
        "overview": "Overview",
        "monitoring": "Project Monitoring",
        "risk": "Risk & Alerts",
        "analytics": "Analytics",
        "search": "Project Search",
    },
    "हिन्दी": {
        "overview": "अवलोकन",
        "monitoring": "परियोजना निगरानी",
        "risk": "जोखिम और अलर्ट",
        "analytics": "विश्लेषण",
        "search": "परियोजना खोज",
    },
    "ਪੰਜਾਬੀ": {
        "overview": "ਸੰਖੇਪ",
        "monitoring": "ਪ੍ਰੋਜੈਕਟ ਨਿਗਰਾਨੀ",
        "risk": "ਖਤਰਾ ਅਤੇ ਅਲਰਟ",
        "analytics": "ਵਿਸ਼ਲੇਸ਼ਣ",
        "search": "ਪ੍ਰੋਜੈਕਟ ਖੋਜ",
    },
}

t = translations[language]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        t["overview"],
        t["monitoring"],
        t["risk"],
        t["analytics"],
        t["search"],
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Dataset: PAIMANA July 2026\n\n"
    "The supplied government CSV contains project coordinates, "
    "budget, time elapsed, fund spent and physical progress."
)

# ============================================================
# OVERVIEW
# ============================================================
if page == t["overview"]:
    st.header("📊 Dashboard Overview")

    total_projects = len(df)
    total_budget = df["Budget"].sum()
    avg_physical = df["Physical Progress Percent"].mean()
    avg_funds = df["Fund Spent Percent"].mean()
    high_risk = (df["Risk_Level"] == "High").sum()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Projects", f"{total_projects:,}")
    c2.metric("Total Budget", f"₹{total_budget:,.2f} Cr")
    c3.metric("Avg. Physical Progress", f"{avg_physical:.1f}%")
    c4.metric("Avg. Funds Spent", f"{avg_funds:.1f}%")
    c5.metric("High Risk Projects", f"{high_risk:,}")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        risk_counts = (
            df["Risk_Level"]
            .value_counts()
            .reindex(["Low", "Medium", "High"], fill_value=0)
            .reset_index()
        )
        risk_counts.columns = ["Risk Level", "Projects"]

        fig_risk = px.bar(
            risk_counts,
            x="Risk Level",
            y="Projects",
            text="Projects",
            title="Projects by Risk Level",
        )
        fig_risk.update_traces(textposition="outside")
        fig_risk.update_layout(
            yaxis_title="Number of Projects",
            xaxis_title="Risk Level",
            height=400,
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with right:
        progress_bins = pd.cut(
            df["Physical Progress Percent"],
            bins=[-1, 25, 50, 75, 100],
            labels=["0–25%", "26–50%", "51–75%", "76–100%"],
        )
        progress_counts = (
            progress_bins.value_counts()
            .sort_index()
            .reset_index()
        )
        progress_counts.columns = ["Progress Range", "Projects"]

        fig_progress = px.bar(
            progress_counts,
            x="Progress Range",
            y="Projects",
            text="Projects",
            title="Physical Progress Distribution",
        )
        fig_progress.update_traces(textposition="outside")
        fig_progress.update_layout(height=400)
        st.plotly_chart(fig_progress, use_container_width=True)

    st.subheader("📋 Dataset Preview")
    preview_cols = [
        "Project ID",
        "Project Name",
        "Budget",
        "Time Elapsed Percent",
        "Fund Spent Percent",
        "Physical Progress Percent",
        "Risk_Level",
    ]
    st.dataframe(
        df[preview_cols].head(20),
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# PROJECT MONITORING
# ============================================================
elif page == t["monitoring"]:
    st.header("🗺️ Project Monitoring")

    st.info(
        "The government CSV provides latitude/longitude for each project, "
        "but it does not provide a State column. Therefore this map uses "
        "the actual coordinates from the source data instead of inventing "
        "state names."
    )

    # Filters
    f1, f2, f3 = st.columns(3)

    with f1:
        risk_filter = st.multiselect(
            "Risk Level",
            ["Low", "Medium", "High"],
            default=["Low", "Medium", "High"],
        )

    with f2:
        min_progress = st.slider(
            "Minimum Physical Progress (%)",
            0,
            100,
            0,
        )

    with f3:
        max_progress = st.slider(
            "Maximum Physical Progress (%)",
            0,
            100,
            100,
        )

    map_df = df[
        df["Risk_Level"].isin(risk_filter)
        & (df["Physical Progress Percent"] >= min_progress)
        & (df["Physical Progress Percent"] <= max_progress)
    ].copy()

    st.metric("Projects currently displayed", f"{len(map_df):,}")

    if len(map_df) > 0:
        center_lat = float(map_df["Lattitude"].mean())
        center_lon = float(map_df["Longitude"].mean())

        fig_map = px.scatter_map(
            map_df,
            lat="Lattitude",
            lon="Longitude",
            color="Risk_Level",
            hover_name="Project Name",
            hover_data={
                "Project ID": True,
                "Budget": ":.2f",
                "Time Elapsed Percent": ":.1f",
                "Fund Spent Percent": ":.1f",
                "Physical Progress Percent": ":.1f",
                "Lattitude": False,
                "Longitude": False,
            },
            center={"lat": center_lat, "lon": center_lon},
            zoom=3.7,
            height=600,
        )

        fig_map.update_layout(
            map_style="open-street-map",
            dragmode="pan",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "displaylogo": False,
                "scrollZoom": True,
                "doubleClick": "reset",
                "responsive": True,
            },
        )
    else:
        st.warning("No projects match the selected filters.")

    st.subheader("📋 Projects")

    display_cols = [
        "Project ID",
        "Project Name",
        "Budget",
        "Time Elapsed Percent",
        "Fund Spent Percent",
        "Physical Progress Percent",
        "Risk_Level",
    ]

    table_df = map_df[display_cols].copy()

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Budget": st.column_config.NumberColumn(
                "Budget (₹ Cr)",
                format="%.2f",
            ),
            "Time Elapsed Percent": st.column_config.NumberColumn(
                "Time Elapsed",
                format="%.1f%%",
            ),
            "Fund Spent Percent": st.column_config.NumberColumn(
                "Funds Spent",
                format="%.1f%%",
            ),
            "Physical Progress Percent": st.column_config.NumberColumn(
                "Physical Progress",
                format="%.1f%%",
            ),
        },
    )

# ============================================================
# RISK & ALERTS
# ============================================================
elif page == t["risk"]:
    st.header("🚨 Risk & Alerts")

    high = df[df["Risk_Level"] == "High"].copy()
    medium = df[df["Risk_Level"] == "Medium"].copy()
    low = df[df["Risk_Level"] == "Low"].copy()

    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 High Risk", len(high))
    c2.metric("🟠 Medium Risk", len(medium))
    c3.metric("🟢 Low Risk", len(low))

    st.markdown("---")

    st.subheader("🔴 High Risk Projects")

    if high.empty:
        st.success("No high-risk projects found.")
    else:
        high_display = high[
            [
                "Project ID",
                "Project Name",
                "Time Elapsed Percent",
                "Physical Progress Percent",
                "Fund Spent Percent",
                "Schedule Gap",
                "Fund Gap",
            ]
        ].sort_values("Schedule Gap", ascending=False)

        st.dataframe(
            high_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Time Elapsed Percent": st.column_config.NumberColumn(
                    "Time Elapsed", format="%.1f%%"
                ),
                "Physical Progress Percent": st.column_config.NumberColumn(
                    "Physical Progress", format="%.1f%%"
                ),
                "Fund Spent Percent": st.column_config.NumberColumn(
                    "Funds Spent", format="%.1f%%"
                ),
                "Schedule Gap": st.column_config.NumberColumn(
                    "Time - Physical Gap", format="%.1f%%"
                ),
                "Fund Gap": st.column_config.NumberColumn(
                    "Fund - Physical Gap", format="%.1f%%"
                ),
            },
        )

    st.subheader("ℹ️ Risk Logic")
    st.markdown(
        """
        **Schedule risk:** physical progress is compared with time elapsed.

        **Financial risk:** funds spent are compared with physical progress.

        - **Low:** both gaps remain below 15 percentage points.
        - **Medium:** at least one gap is 15–29.9 percentage points.
        - **High:** at least one gap is 30 percentage points or more,
          or the combined risk score reaches the high-risk threshold.
        """
    )

# ============================================================
# ANALYTICS
# ============================================================
elif page == t["analytics"]:
    st.header("📈 Analytics")

    st.subheader("⏱️ Time Elapsed vs Physical Progress — Trend")

    # Create 10% time-elapsed bands so the trend is structured and readable.
    trend_df = df[
        ["Time Elapsed Percent", "Physical Progress Percent"]
    ].dropna().copy()

    bins = list(range(0, 101, 10))
    labels = [f"{i}-{i + 10}%" for i in range(0, 100, 10)]

    trend_df["Time Band"] = pd.cut(
        trend_df["Time Elapsed Percent"].clip(0, 100),
        bins=bins,
        labels=labels,
        include_lowest=True,
        right=True,
    )

    progress_trend = (
        trend_df.groupby("Time Band", observed=False)["Physical Progress Percent"]
        .agg(["mean", "count"])
        .reset_index()
    )

    progress_trend.columns = [
        "Time Band",
        "Average Physical Progress",
        "Project Count",
    ]

    # Middle of each band gives a clean x-coordinate for the line.
    progress_trend["Time Midpoint"] = [
        i + 5 for i in range(0, 100, 10)
    ]

    fig1 = px.line(
        progress_trend,
        x="Time Midpoint",
        y="Average Physical Progress",
        markers=True,
        title="Average Physical Progress by Time Elapsed",
        hover_data={
            "Time Midpoint": False,
            "Average Physical Progress": ":.1f",
            "Project Count": True,
        },
    )

    fig1.update_traces(
        line=dict(width=4),
        marker=dict(size=9),
        hovertemplate=(
            "<b>Time Band: %{customdata[1]}</b><br>"
            "Average Physical Progress: %{y:.1f}%<br>"
            "Projects: %{customdata[0]:,}"
            "<extra></extra>"
        ),
    )

    # Add the actual band labels to hover data explicitly.
    fig1.data[0].customdata = [
        [count, band]
        for count, band in zip(
            progress_trend["Project Count"],
            progress_trend["Time Band"].astype(str),
        )
    ]

    fig1.update_layout(
        xaxis_title="Time Elapsed (%)",
        yaxis_title="Average Physical Progress (%)",
        xaxis=dict(
            range=[0, 100],
            tickmode="array",
            tickvals=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
            ticktext=labels,
            fixedrange=False,
        ),
        yaxis=dict(
            range=[0, 100],
            dtick=20,
            fixedrange=False,
        ),
        height=500,
        margin=dict(t=70, b=90, l=60, r=30),
        hovermode="x",
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "doubleClick": "reset",
            "responsive": True,
        },
        key="time_physical_trend",
    )

    st.subheader("💰 Funds Spent vs Physical Progress")

    fig2 = px.scatter(
        df,
        x="Fund Spent Percent",
        y="Physical Progress Percent",
        hover_name="Project Name",
        hover_data={
            "Project ID": True,
            "Time Elapsed Percent": ":.1f",
            "Budget": ":.2f",
        },
        title="Funds Spent vs Physical Progress",
    )
    fig2.update_layout(
        xaxis_title="Funds Spent (%)",
        yaxis_title="Physical Progress (%)",
        xaxis=dict(range=[0, 100]),
        yaxis=dict(range=[0, 100]),
        height=500,
    )
    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "doubleClick": "reset",
        },
    )

    # IMPORTANT:
    # The government CSV does not contain State.
    # So these charts are based on the actual dataset-wide records,
    # not fabricated state labels.
    st.subheader("📊 Overall Progress Metrics")

    metric_df = pd.DataFrame(
        {
            "Metric": [
                "Time Elapsed",
                "Funds Spent",
                "Physical Progress",
            ],
            "Average (%)": [
                df["Time Elapsed Percent"].mean(),
                df["Fund Spent Percent"].mean(),
                df["Physical Progress Percent"].mean(),
            ],
        }
    )

    fig3 = px.bar(
        metric_df,
        x="Metric",
        y="Average (%)",
        text="Average (%)",
        title="Overall Average Project Metrics",
    )
    fig3.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
    )
    fig3.update_layout(
        yaxis_title="Percentage (%)",
        yaxis=dict(range=[0, 100]),
        height=420,
        margin=dict(t=70, b=50, l=50, r=30),
    )
    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "doubleClick": "reset",
        },
    )

# ============================================================
# PROJECT SEARCH
# ============================================================
else:
    st.header("🔎 Project Search")

    query = st.text_input(
        "Search by Project ID or Project Name",
        placeholder="Enter project name or ID...",
    )

    search_df = df.copy()

    if query.strip():
        q = query.strip()

        name_match = search_df["Project Name"].str.contains(
            q,
            case=False,
            na=False,
            regex=False,
        )

        id_match = search_df["Project ID"].astype(str).str.contains(
            q,
            case=False,
            na=False,
            regex=False,
        )

        search_df = search_df[name_match | id_match]

    risk_filter = st.multiselect(
        "Filter by Risk",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"],
    )

    search_df = search_df[search_df["Risk_Level"].isin(risk_filter)]

    st.write(f"**{len(search_df):,} project(s) found**")

    if search_df.empty:
        st.warning("No matching projects found.")
    else:
        for _, row in search_df.head(100).iterrows():
            with st.expander(
                f"#{int(row['Project ID'])} — {row['Project Name'][:120]}"
            ):
                c1, c2, c3, c4 = st.columns(4)

                c1.metric("Budget", f"₹{row['Budget']:,.2f} Cr")
                c2.metric(
                    "Time Elapsed",
                    f"{row['Time Elapsed Percent']:.1f}%"
                    if pd.notna(row["Time Elapsed Percent"])
                    else "N/A",
                )
                c3.metric(
                    "Funds Spent",
                    f"{row['Fund Spent Percent']:.1f}%",
                )
                c4.metric(
                    "Physical Progress",
                    f"{row['Physical Progress Percent']:.1f}%",
                )

                st.write(f"**Risk:** {row['Risk_Level']}")
                st.write(
                    f"**Coordinates:** "
                    f"{row['Lattitude']:.4f}, {row['Longitude']:.4f}"
                )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    "MoSPI PAIMANA Portal • Built for project monitoring and decision support"
)
