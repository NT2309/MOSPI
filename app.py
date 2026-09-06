import os
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# MULTILINGUAL DICTIONARY ENGINE
# =========================================================
TRANSLATIONS = {
    "English": {
        "title": "🏗️ MoSPI PAIMANA Portal",
        "subtitle": "Integrated Project Monitoring & Analytics Platform",
        "support": "🎧 Support",
        "tech_help": "📞 Technical Helpdesk",
        "help_desc": "For dashboard assistance or reporting discrepancies:",
        "help_time": "Mon–Fri | 9:00 AM – 5:30 PM IST",
        "user_type": "User Type",
        "gov_off": "Government Official",
        "citizen": "Citizen",
        "nav_title": "📌 Navigation",
        "lang_select": "🌐 Select Language",
        "go_to": "Go to",
        "page_overview": "Overview",
        "page_state": "State-wise Monitoring",
        "page_risk": "Risk & Alerts",
        "page_analytics": "Analytics",
        "page_search": "Project Search",
        "projects_loaded": "Projects Loaded",
        "data_source": "Data Source: PAIMANA Project Dataset",
        "proj_details": "📋 Project Details",
        "proj_id": "Project ID",
        "proj_name": "Project",
        "state": "State",
        "budget": "Budget",
        "time_elapsed": "Time Elapsed",
        "funds_spent": "Funds Spent",
        "phys_progress": "Physical Progress",
        "risk": "Risk",
        "score": "Score",
        "phys_progress_hdr": "Physical Progress",
        "crit_warn": "🚨 Critical Warning: Physical progress is {gap:.1f}% behind the elapsed timeline.",
        "warn": "⚠️ Warning: Physical progress is {gap:.1f}% behind the elapsed timeline.",
        "success_thresh": "🟢 Project progress is currently within the monitoring threshold.",
        "hdr_overview": "📊 Project Overview",
        "total_proj": "Total Projects",
        "total_budget": "Total Budget",
        "avg_progress": "Avg Physical Progress",
        "high_crit_risk": "High / Critical Risk",
        "state_summary": "🇮🇳 State-wise Project Summary",
        "projects_col": "Projects",
        "budget_cr_col": "Budget (₹ Cr)",
        "avg_prog_col": "Avg Progress (%)",
        "avg_funds_col": "Avg Funds Spent (%)",
        "proj_by_state": "Projects by State",
        "num_projects": "Number of Projects",
        "hdr_state_mon": "🗺️ State-wise Project Monitoring",
        "select_state": "Select State",
        "all_states": "All States",
        "proj_locations": "📍 Project Locations",
        "no_coords": "No geographical coordinates available.",
        "projects_hdr": "📋 Projects",
        "details_btn": "Details",
        "hdr_risk_alerts": "🚨 Risk & Early Warning Centre",
        "risk_desc": "Automated monitoring engine identifies projects requiring early intervention.",
        "critical": "🚨 Critical",
        "high": "🔴 High",
        "medium": "🟡 Medium",
        "low": "🟢 Low",
        "req_attention": "⚠️ Projects Requiring Attention",
        "no_high_risk": "🟢 No high-risk projects detected.",
        "time_gap_lbl": "Time-progress gap",
        "funds_gap_lbl": "Funds-progress gap",
        "hdr_analytics": "📈 Comparative Analytics",
        "time_vs_prog": "⏱️ Time Elapsed vs Physical Progress",
        "prog_performance": "Project Progress Performance",
        "diag_info": "Projects below the diagonal line are progressing slower than their elapsed timeline.",
        "funds_vs_prog": "💰 Funds Spent vs Physical Progress",
        "fin_vs_phys": "Financial vs Physical Progress",
        "state_perf": "🏛️ State-wise Performance",
        "state_vs_funds": "State-wise Physical Progress vs Funds Spent",
        "hdr_search": "🔎 Project Search",
        "search_label": "Search by Project Name, Project ID or State",
        "search_ph": "e.g. Punjab / Haryana / P001",
        "found_proj": "Found **{count}** project(s)",
        "no_match": "No matching projects found.",
        "footer": "MoSPI PAIMANA Portal | SIH Prototype | Project Monitoring & Early Warning System",
    },
    "Hindi": {
        "title": "🏗️ एमओएसपीआई पैमाना पोर्टल",
        "subtitle": "एकीकृत परियोजना निगरानी और विश्लेषण मंच",
        "support": "🎧 सहायता",
        "tech_help": "📞 तकनीकी हेल्पडेस्क",
        "help_desc": "डैशबोर्ड सहायता या विसंगतियों की रिपोर्टिंग के लिए:",
        "help_time": "सोम-शुक्र | सुबह 9:00 - शाम 5:30 IST",
        "user_type": "उपयोगकर्ता का प्रकार",
        "gov_off": "सरकारी अधिकारी",
        "citizen": "नागरिक",
        "nav_title": "📌 नेविगेशन",
        "lang_select": "🌐 भाषा चुनें",
        "go_to": "नेविगेट करें",
        "page_overview": "अवलोकन (Overview)",
        "page_state": "राज्य-वार निगरानी",
        "page_risk": "जोखिम और अलर्ट",
        "page_analytics": "विश्लेषण (Analytics)",
        "page_search": "परियोजना खोजें",
        "projects_loaded": "कुल लोड की गई परियोजनाएं",
        "data_source": "डेटा स्रोत: पैमाना प्रोजेक्ट डेटासेट",
        "proj_details": "📋 परियोजना विवरण",
        "proj_id": "परियोजना आईडी",
        "proj_name": "परियोजना",
        "state": "राज्य",
        "budget": "बजट",
        "time_elapsed": "बीता हुआ समय",
        "funds_spent": "खर्च किया गया धन",
        "phys_progress": "भौतिक प्रगति",
        "risk": "जोखिम स्तर",
        "score": "स्कोर",
        "phys_progress_hdr": "भौतिक प्रगति",
        "crit_warn": "🚨 गंभीर चेतावनी: भौतिक प्रगति समयसीमा से {gap:.1f}% पीछे है।",
        "warn": "⚠️ चेतावनी: भौतिक प्रगति समयसीमा से {gap:.1f}% पीछे है।",
        "success_thresh": "🟢 परियोजना की प्रगति वर्तमान में स्वीकार्य सीमा के भीतर है।",
        "hdr_overview": "📊 परियोजना अवलोकन",
        "total_proj": "कुल परियोजनाएं",
        "total_budget": "कुल बजट",
        "avg_progress": "औसत भौतिक प्रगति",
        "high_crit_risk": "उच्च / गंभीर जोखिम",
        "state_summary": "🇮🇳 राज्यवार परियोजना सारांश",
        "projects_col": "परियोजनाएं",
        "budget_cr_col": "बजट (₹ करोड़)",
        "avg_prog_col": "औसत प्रगति (%)",
        "avg_funds_col": "औसत खर्च धन (%)",
        "proj_by_state": "राज्य के अनुसार परियोजनाएं",
        "num_projects": "परियोजनाओं की संख्या",
        "hdr_state_mon": "🗺️ राज्य-वार परियोजना निगरानी",
        "select_state": "राज्य चुनें",
        "all_states": "सभी राज्य",
        "proj_locations": "📍 परियोजना का स्थान",
        "no_coords": "कोई भौगोलिक निर्देशांक उपलब्ध नहीं हैं।",
        "projects_hdr": "📋 परियोजना सूची",
        "details_btn": "विवरण",
        "hdr_risk_alerts": "🚨 जोखिम और चेतावनी केंद्र",
        "risk_desc": "स्वचालित निगरानी प्रणाली उन परियोजनाओं की पहचान करती है जिनमें त्वरित ध्यान देने की आवश्यकता है।",
        "critical": "🚨 गंभीर (Critical)",
        "high": "🔴 उच्च (High)",
        "medium": "🟡 मध्यम (Medium)",
        "low": "🟢 कम (Low)",
        "req_attention": "⚠️ ध्यान देने योग्य परियोजनाएं",
        "no_high_risk": "🟢 कोई उच्च जोखिम वाली परियोजना नहीं पाई गई।",
        "time_gap_lbl": "समय-प्रगति अंतर",
        "funds_gap_lbl": "धन-प्रगति अंतर",
        "hdr_analytics": "📈 तुलनात्मक विश्लेषण",
        "time_vs_prog": "⏱️ बीता हुआ समय बनाम भौतिक प्रगति",
        "prog_performance": "परियोजना प्रगति प्रदर्शन",
        "diag_info": "विकर्ण रेखा के नीचे की परियोजनाएं अपनी समय सीमा की तुलना में धीमी गति से आगे बढ़ रही हैं।",
        "funds_vs_prog": "💰 खर्च किया गया धन बनाम भौतिक प्रगति",
        "fin_vs_phys": "वित्तीय बनाम भौतिक प्रगति",
        "state_perf": "🏛️ राज्य-वार प्रदर्शन",
        "state_vs_funds": "राज्यवार भौतिक प्रगति बनाम खर्च किया गया धन",
        "hdr_search": "🔎 परियोजना खोज",
        "search_label": "परियोजना का नाम, आईडी या राज्य खोजें",
        "search_ph": "उदा. पंजाब / हरियाणा / P001",
        "found_proj": "कुल **{count}** परियोजनाएं मिलीं",
        "no_match": "कोई मेल खाने वाली परियोजना नहीं मिली।",
        "footer": "एमओएसपीआई पैमाना पोर्टल | एसआईएच प्रोटोटाइप | परियोजना निगरानी और पूर्व चेतावनी प्रणाली",
    },
    "Punjabi": {
        "title": "🏗️ ਐਮਓਐਸਪੀਆਈ ਪੈਮਾਨਾ ਪੋਰਟਲ",
        "subtitle": "ਏਕੀਕ੍ਰਿਤ ਪ੍ਰੋਜੈਕਟ ਨਿਗਰਾਨੀ ਅਤੇ ਵਿਸ਼ਲੇਸ਼ਣ ਪਲੇਟਫਾਰਮ",
        "support": "🎧 ਸਹਾਇਤਾ",
        "tech_help": "📞 ਤਕਨੀਕੀ ਹੈਲਪਦੇਸਕ",
        "help_desc": "ਡੈਸ਼ਬੋਰਡ ਸਹਾਇਤਾ ਜਾਂ ਸਮੱਸਿਆਵਾਂ ਦੀ ਰਿਪੋਰਟ ਕਰਨ ਲਈ:",
        "help_time": "ਸੋਮ-ਸ਼ੁੱਕਰ | ਸਵੇਰੇ 9:00 - ਸ਼ਾਮ 5:30 IST",
        "user_type": "ਉਪਭੋਗਤਾ ਦੀ ਕਿਸਮ",
        "gov_off": "ਸਰਕਾਰੀ ਅਧਿਕਾਰੀ",
        "citizen": "ਨਾਗਰਿਕ",
        "nav_title": "📌 ਨੈਵੀਗੇਸ਼ਨ",
        "lang_select": "🌐 ਭਾਸ਼ਾ ਚੁਣੋ",
        "go_to": "ਨੈਵੀਗੇਟ ਕਰੋ",
        "page_overview": "ਸੰਖੇਪ (Overview)",
        "page_state": "ਰਾਜ-ਵਾਰ ਨਿਗਰਾਨੀ",
        "page_risk": "ਜੋਖਮ ਅਤੇ ਅਲਰਟ",
        "page_analytics": "ਵਿਸ਼ਲੇਸ਼ਣ (Analytics)",
        "page_search": "ਪ੍ਰੋਜੈਕਟ ਖੋਜੋ",
        "projects_loaded": "ਕੁੱਲ ਲੋਡ ਕੀਤੇ ਪ੍ਰੋਜੈਕਟ",
        "data_source": "ਡਾਟਾ ਸਰੋਤ: ਪੈਮਾਨਾ ਪ੍ਰੋਜੈਕਟ ਡਾਟਾਸੈਟ",
        "proj_details": "📋 ਪ੍ਰੋਜੈਕਟ ਦੇ ਵੇਰਵੇ",
        "proj_id": "ਪ੍ਰੋਜੈਕਟ ਆਈਡੀ",
        "proj_name": "ਪ੍ਰੋਜੈਕਟ",
        "state": "ਰਾਜ",
        "budget": "ਬਜਟ",
        "time_elapsed": "ਬੀਤਿਆ ਸਮਾਂ",
        "funds_spent": "ਖਰਚਿਆ ਗਿਆ ਫੰਡ",
        "phys_progress": "ਭੌਤਿਕ ਪ੍ਰਗਤੀ",
        "risk": "ਜੋਖਮ ਦਾ ਪੱਧਰ",
        "score": "ਸਕੋਰ",
        "phys_progress_hdr": "ਭੌਤਿਕ ਪ੍ਰਗਤੀ",
        "crit_warn": "🚨 ਗੰਭੀਰ ਚੇਤਾਵਨੀ: ਭੌਤਿਕ ਪ੍ਰਗਤੀ ਸਮੇਂ ਦੀ ਰੇਖਾ ਤੋਂ {gap:.1f}% ਪਿੱਛੇ ਹੈ।",
        "warn": "⚠️ ਚੇਤਾਵਨੀ: ਭੌਤਿਕ ਪ੍ਰਗਤੀ ਸਮੇਂ ਦੀ ਰੇਖਾ ਤੋਂ {gap:.1f}% ਪਿੱਛੇ ਹੈ।",
        "success_thresh": "🟢 ਪ੍ਰੋਜੈਕਟ ਦੀ ਪ੍ਰਗਤੀ ਫਿਲਹਾਲ ਨਿਗਰਾਨੀ ਦੀ ਸੀਮਾ ਦੇ ਅੰਦਰ ਹੈ।",
        "hdr_overview": "📊 ਪ੍ਰੋਜੈਕਟ ਸੰਖੇਪ",
        "total_proj": "ਕੁੱਲ ਪ੍ਰੋਜੈਕਟ",
        "total_budget": "ਕੁੱਲ ਬਜਟ",
        "avg_progress": "ਔਸਤ ਭੌਤਿਕ ਪ੍ਰਗਤੀ",
        "high_crit_risk": "ਉੱਚ / ਗੰਭੀਰ ਜੋਖਮ",
        "state_summary": "🇮🇳 ਰਾਜ-ਵਾਰ ਪ੍ਰੋਜੈਕਟ ਸਾਰਾਂਸ਼",
        "projects_col": "ਪ੍ਰੋਜੈਕਟ",
        "budget_cr_col": "ਬਜਟ (₹ ਕਰੋੜ)",
        "avg_prog_col": "ਔਸਤ ਪ੍ਰਗਤੀ (%)",
        "avg_funds_col": "ਔਸਤ ਖਰਚਿਆ ਫੰਡ (%)",
        "proj_by_state": "ਰਾਜ ਅਨੁਸਾਰ ਪ੍ਰੋਜੈਕਟ",
        "num_projects": "ਪ੍ਰੋਜੈਕਟਾਂ ਦੀ ਗਿਣਤੀ",
        "hdr_state_mon": "🗺️ ਰਾਜ-ਵਾਰ ਪ੍ਰੋਜੈਕਟ ਨਿਗਰਾਨੀ",
        "select_state": "ਰਾਜ ਚੁਣੋ",
        "all_states": "ਸਾਰੇ ਰਾਜ",
        "proj_locations": "📍 ਪ੍ਰੋਜੈਕਟ ਦਾ ਸਥਾਨ",
        "no_coords": "ਕੋਈ ਭੂਗੋਲਿਕ ਨਿਰਦੇਸ਼ਾਂਕ ਉਪਲਬਧ ਨਹੀਂ ਹਨ।",
        "projects_hdr": "📋 ਪ੍ਰੋਜੈਕਟ ਸੂਚੀ",
        "details_btn": "ਵੇਰਵੇ",
        "hdr_risk_alerts": "🚨 ਜੋਖਮ ਅਤੇ ਚੇਤਾਵਨੀ ਕੇਂਦਰ",
        "risk_desc": "ਸਵੈਚਾਲਿਤ ਨਿਗਰਾਨੀ ਪ੍ਰਣਾਲੀ ਉਹਨਾਂ ਪ੍ਰੋਜੈਕਟਾਂ ਦੀ ਪਛਾਣ ਕਰਦੀ ਹੈ ਜਿਨ੍ਹਾਂ 'ਤੇ ਤੁਰੰਤ ਧਿਆਨ ਦੇਣ ਦੀ ਲੋੜ ਹੈ।",
        "critical": "🚨 ਗੰਭੀਰ (Critical)",
        "high": "🔴 ਉੱਚ (High)",
        "medium": "🟡 ਮੱਧਮ (Medium)",
        "low": "🟢 ਘੱਟ (Low)",
        "req_attention": "⚠️ ਧਿਆਨ ਦੇਣ ਯੋਗ ਪ੍ਰੋਜੈਕਟ",
        "no_high_risk": "🟢 ਕੋਈ ਉੱਚ-ਜੋਖਮ ਵਾਲਾ ਪ੍ਰੋਜੈਕਟ ਨਹੀਂ ਮਿਲਿਆ।",
        "time_gap_lbl": "ਸਮਾਂ-ਪ੍ਰਗਤੀ ਦਾ ਅੰਤਰ",
        "funds_gap_lbl": "ਫੰਡ-ਪ੍ਰਗਤੀ ਦਾ ਅੰਤਰ",
        "hdr_analytics": "📈 ਤੁਲਨਾਤਮਕ ਵਿਸ਼ਲੇਸ਼ਣ",
        "time_vs_prog": "⏱️ ਬੀਤਿਆ ਸਮਾਂ ਬਨਾਮ ਭੌਤਿਕ ਪ੍ਰਗਤੀ",
        "prog_performance": "ਪ੍ਰੋਜੈਕਟ ਪ੍ਰਗਤੀ ਦਾ ਪ੍ਰਦਰਸ਼ਨ",
        "diag_info": "ਤਰਛੀ ਲਾਈਨ ਤੋਂ ਹੇਠਾਂ ਵਾਲੇ ਪ੍ਰੋਜੈਕਟ ਆਪਣੀ ਸਮਾਂ ਸੀਮਾ ਨਾਲੋਂ ਹੌਲੀ ਚੱਲ ਰਹੇ ਹਨ।",
        "funds_vs_prog": "💰 ਖਰਚਿਆ ਫੰਡ ਬਨਾਮ ਭੌਤਿਕ ਪ੍ਰਗਤੀ",
        "fin_vs_phys": "ਵਿੱਤੀ ਬਨਾਮ ਭੌਤਿਕ ਪ੍ਰਗਤੀ",
        "state_perf": "🏛️ ਰਾਜ-ਵਾਰ ਪ੍ਰਦਰਸ਼ਨ",
        "state_vs_funds": "ਰਾਜ-ਵਾਰ ਭੌਤਿਕ ਪ੍ਰਗਤੀ ਬਨਾਮ ਖਰਚਿਆ ਫੰਡ",
        "hdr_search": "🔎 ਪ੍ਰੋਜੈਕਟ ਖੋਜ",
        "search_label": "ਪ੍ਰੋਜੈਕਟ ਦਾ ਨਾਮ, ਆਈਡੀ ਜਾਂ ਰਾਜ ਖੋਜੋ",
        "search_ph": "ਉਦਾਹਰਨ: ਪੰਜਾਬ / ਹਰਿਆਣਾ / P001",
        "found_proj": "ਕੁੱਲ **{count}** ਪ੍ਰੋਜੈਕਟ ਮਿਲੇ",
        "no_match": "ਕੋਈ ਮੇਲ ਖਾਂਦਾ ਪ੍ਰੋਜੈਕਟ ਨਹੀਂ ਮਿਲਿਆ।",
        "footer": "ਐਮਓਐਸਪੀਆਈ ਪੈਮਾਨਾ ਪੋਰਟਲ | ਐਸਆਈਹ ਪ੍ਰੋਟੋਟਾਈਪ | ਪ੍ਰੋਜੈਕਟ ਨਿਗਰਾਨੀ ਅਤੇ ਚੇਤਾਵਨੀ ਪ੍ਰਣਾਲੀ",
    }
}

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="MoSPI PAIMANA Portal",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function for translations
def t(key, **kwargs):
    lang = st.session_state.get("language_select_box", "English")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, TRANSLATIONS["English"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text

# =========================================================
# SIDEBAR LANGUAGE & NAVIGATION SETUP
# =========================================================
# 1. Language Selection Box (Direct Session State binding)
selected_language = st.sidebar.selectbox(
    "🌐 Language / भाषा / ਭਾਸ਼ਾ",
    ["English", "Hindi", "Punjabi"],
    key="language_select_box"
)

st.sidebar.title(t("nav_title"))

# 2. Stable Internal Navigation Keys
PAGE_KEYS = ["Overview", "State-wise Monitoring", "Risk & Alerts", "Analytics", "Project Search"]
PAGE_TRANSLATION_MAP = {
    "Overview": "page_overview",
    "State-wise Monitoring": "page_state",
    "Risk & Alerts": "page_risk",
    "Analytics": "page_analytics",
    "Project Search": "page_search"
}

# Dynamic Translation via format_func
page = st.sidebar.radio(
    t("go_to"),
    PAGE_KEYS,
    format_func=lambda key: t(PAGE_TRANSLATION_MAP[key]),
    key="nav_radio"
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
# LOAD CSV DATASET
# =========================================================
CSV_FILE = "punjab_haryana_projects.csv"

if not os.path.exists(CSV_FILE):
    downloads_file = os.path.join(
        os.path.expanduser("~"),
        "Downloads",
        CSV_FILE
    )

    if os.path.exists(downloads_file):
        CSV_FILE = downloads_file
    else:
        st.error(
            "CSV file nahi mila. "
            "punjab_haryana_projects.csv ko app.py ke same folder mein rakho."
        )
        st.stop()

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

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error("CSV mein ye columns missing hain: " + ", ".join(missing_columns))
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
    df[column] = pd.to_numeric(df[column], errors="coerce")

# =========================================================
# RISK CALCULATION ENGINE
# =========================================================
def calculate_risk(row):
    time_elapsed = row["Time_Elapsed_Percent"] if pd.notna(row["Time_Elapsed_Percent"]) else 0
    physical_progress = row["Physical_Progress_Percent"] if pd.notna(row["Physical_Progress_Percent"]) else 0
    funds_spent = row["Funds_Spent_Percent"] if pd.notna(row["Funds_Spent_Percent"]) else 0

    score = 0

    time_gap = time_elapsed - physical_progress
    if time_gap >= 30:
        score += 50
    elif time_gap >= 15:
        score += 30
    elif time_gap >= 5:
        score += 15

    spending_gap = funds_spent - physical_progress
    if spending_gap >= 25:
        score += 30
    elif spending_gap >= 10:
        score += 15

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

risk_results = df.apply(calculate_risk, axis=1)
df["Risk_Score"] = [r[0] for r in risk_results]
df["Risk_Level"] = [r[1] for r in risk_results]

# SIDEBAR FOOTER METRICS
st.sidebar.divider()
st.sidebar.metric(t("projects_loaded"), len(df))
st.sidebar.caption(t("data_source"))

# =========================================================
# HEADER & USER TYPE SELECTOR
# =========================================================
header1, header2, header3 = st.columns([5, 1.2, 1.2])

with header1:
    st.markdown(f'<div class="main-title">{t("title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{t("subtitle")}</div>', unsafe_allow_html=True)

with header2:
    with st.popover(t("support")):
        st.markdown(f"### {t('tech_help')}")
        st.write(t("help_desc"))
        st.write("📧 support-paimana@mospi.gov.in")
        st.write("📞 1800-11-2026")
        st.caption(t("help_time"))

# FIXED KEYS for User Roles (Prevents User-Type Glitch during language switches)
USER_ROLE_KEYS = ["gov_off", "citizen"]

with header3:
    role_key = st.selectbox(
        t("user_type"),
        USER_ROLE_KEYS,
        format_func=lambda key: t(key),
        key="user_type_select"
    )

st.divider()

# =========================================================
# PROJECT DETAILS FUNCTION
# =========================================================
def show_project_details(row):
    st.markdown(f"### {t('proj_details')}")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**{t('proj_id')}:** {row['Project_ID']}")
        st.write(f"**{t('proj_name')}:** {row['Project_Name']}")
        st.write(f"**{t('state')}:** {row['State']}")
        st.write(f"**{t('budget')}:** ₹{row['Budget_Crores']:,.2f} Cr")

    with col2:
        st.write(f"**{t('time_elapsed')}:** {row['Time_Elapsed_Percent']:.1f}%")
        st.write(f"**{t('funds_spent')}:** {row['Funds_Spent_Percent']:.1f}%")
        st.write(f"**{t('phys_progress')}:** {row['Physical_Progress_Percent']:.1f}%")
        
        risk_label_map = {
            "Critical": t("critical"),
            "High": t("high"),
            "Medium": t("medium"),
            "Low": t("low")
        }
        translated_risk = risk_label_map.get(row['Risk_Level'], row['Risk_Level'])
        st.write(f"**{t('risk')}:** {translated_risk} ({row['Risk_Score']}/100)")

    st.write(f"#### {t('phys_progress_hdr')}")

    progress_value = int(min(max(row["Physical_Progress_Percent"], 0), 100))
    st.progress(progress_value)

    time_gap = row["Time_Elapsed_Percent"] - row["Physical_Progress_Percent"]

    if time_gap >= 30:
        st.error(t("crit_warn", gap=time_gap))
    elif time_gap >= 15:
        st.warning(t("warn", gap=time_gap))
    else:
        st.success(t("success_thresh"))

# =========================================================
# OVERVIEW PAGE
# =========================================================
if page == "Overview":
    st.header(t("hdr_overview"))

    total_projects = len(df)
    total_budget = df["Budget_Crores"].sum()
    average_progress = df["Physical_Progress_Percent"].mean()
    high_risk_projects = len(df[df["Risk_Level"].isin(["High", "Critical"])])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(t("total_proj"), f"{total_projects:,}")

    with col2:
        st.metric(t("total_budget"), f"₹{total_budget:,.0f} Cr")

    with col3:
        st.metric(t("avg_progress"), f"{average_progress:.1f}%")

    with col4:
        st.metric(t("high_crit_risk"), f"{high_risk_projects:,}")

    st.divider()

    st.subheader(t("state_summary"))

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

    state_summary["Budget_Cr"] = state_summary["Budget_Cr"].round(2)
    state_summary["Avg_Progress"] = state_summary["Avg_Progress"].round(1)
    state_summary["Avg_Funds_Spent"] = state_summary["Avg_Funds_Spent"].round(1)

    display_summary = state_summary.rename(
        columns={
            "State": t("state"),
            "Projects": t("projects_col"),
            "Budget_Cr": t("budget_cr_col"),
            "Avg_Progress": t("avg_prog_col"),
            "Avg_Funds_Spent": t("avg_funds_col")
        }
    )

    st.table(display_summary)

    fig = px.bar(
        state_summary,
        x="State",
        y="Projects",
        text="Projects",
        title=t("proj_by_state")
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title=t("state"),
        yaxis_title=t("num_projects"),
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# STATE-WISE MONITORING PAGE
# =========================================================
elif page == "State-wise Monitoring":
    st.header(t("hdr_state_mon"))

    states = sorted(df["State"].dropna().unique().tolist())
    state_options = ["ALL"] + states

    selected_state_key = st.selectbox(
        t("select_state"),
        state_options,
        format_func=lambda s: t("all_states") if s == "ALL" else s,
        key="state_select_box"
    )

    if selected_state_key == "ALL":
        state_df = df.copy()
    else:
        state_df = df[df["State"] == selected_state_key].copy()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(t("projects_col"), f"{len(state_df):,}")

    with col2:
        budget_value = state_df["Budget_Crores"].sum()
        st.metric(t("budget"), f"₹{budget_value:,.0f} Cr")

    with col3:
        progress_value = state_df["Physical_Progress_Percent"].mean()
        st.metric(t("phys_progress"), f"{progress_value:.1f}%")

    with col4:
        funds_value = state_df["Funds_Spent_Percent"].mean()
        st.metric(t("funds_spent"), f"{funds_value:.1f}%")

    st.divider()

    st.subheader(t("proj_locations"))
    map_df = state_df.dropna(subset=["Lat", "Lon"])

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
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info(t("no_coords"))

    st.subheader(t("projects_hdr"))

    for index, row in state_df.reset_index(drop=True).iterrows():
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.markdown(f"**{row['Project_Name']}**")
                st.caption(f"{row['Project_ID']} • {row['State']}")

            with col2:
                st.write(f"{t('phys_progress')}: **{row['Physical_Progress_Percent']:.1f}%**")

            with col3:
                st.write(f"{t('risk')}: **{row['Risk_Level']}**")
                st.caption(f"{t('score')}: {row['Risk_Score']}/100")

            with col4:
                details_key = f"state_details_{row['Project_ID']}_{index}"

                if st.button(t("details_btn"), key=details_key):
                    st.session_state["selected_project_id"] = row["Project_ID"]

            if st.session_state.get("selected_project_id") == row["Project_ID"]:
                show_project_details(row)

# =========================================================
# RISK & ALERTS PAGE
# =========================================================
elif page == "Risk & Alerts":
    st.header(t("hdr_risk_alerts"))
    st.write(t("risk_desc"))

    risk_counts = (
        df["Risk_Level"]
        .value_counts()
        .reindex(["Critical", "High", "Medium", "Low"], fill_value=0)
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(t("critical"), int(risk_counts["Critical"]))

    with col2:
        st.metric(t("high"), int(risk_counts["High"]))

    with col3:
        st.metric(t("medium"), int(risk_counts["Medium"]))

    with col4:
        st.metric(t("low"), int(risk_counts["Low"]))

    st.divider()

    alert_df = df[df["Risk_Level"].isin(["Critical", "High"])].sort_values("Risk_Score", ascending=False)

    st.subheader(t("req_attention"))

    if alert_df.empty:
        st.success(t("no_high_risk"))
    else:
        for _, row in alert_df.iterrows():
            if row["Risk_Level"] == "Critical":
                st.error(f"🚨 {row['Project_Name']} | {row['State']} | {t('score')}: {row['Risk_Score']}/100")
            else:
                st.warning(f"⚠️ {row['Project_Name']} | {row['State']} | {t('score')}: {row['Risk_Score']}/100")

            time_gap = row["Time_Elapsed_Percent"] - row["Physical_Progress_Percent"]
            spending_gap = row["Funds_Spent_Percent"] - row["Physical_Progress_Percent"]

            st.caption(
                f"{t('time_gap_lbl')}: {time_gap:.1f}% | "
                f"{t('funds_gap_lbl')}: {spending_gap:.1f}%"
            )

# =========================================================
# ANALYTICS PAGE
# =========================================================
elif page == "Analytics":
    st.header(t("hdr_analytics"))

    st.subheader(t("time_vs_prog"))

    fig1 = px.scatter(
        df,
        x="Time_Elapsed_Percent",
        y="Physical_Progress_Percent",
        size="Budget_Crores",
        color="Risk_Level",
        hover_name="Project_Name",
        hover_data=["Project_ID", "State"],
        title=t("prog_performance")
    )

    fig1.add_shape(
        type="line",
        x0=0, y0=0, x1=100, y1=100,
        line=dict(dash="dash")
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.info(t("diag_info"))

    st.subheader(t("funds_vs_prog"))

    fig2 = px.scatter(
        df,
        x="Funds_Spent_Percent",
        y="Physical_Progress_Percent",
        size="Budget_Crores",
        color="State",
        hover_name="Project_Name",
        hover_data=["Project_ID"],
        title=t("fin_vs_phys")
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader(t("state_perf"))

    performance = (
        df.groupby("State")
        .agg(
            Physical_Progress=("Physical_Progress_Percent", "mean"),
            Funds_Spent=("Funds_Spent_Percent", "mean")
        )
        .reset_index()
    )

    fig3 = px.bar(
        performance,
        x="State",
        y=["Physical_Progress", "Funds_Spent"],
        barmode="group",
        title=t("state_vs_funds")
    )

    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# PROJECT SEARCH PAGE
# =========================================================
elif page == "Project Search":
    st.header(t("hdr_search"))

    search = st.text_input(
        t("search_label"),
        placeholder=t("search_ph"),
        key="search_input_field"
    )

    filtered_df = df.copy()

    if search.strip():
        search_text = search.strip().lower()
        filtered_df = filtered_df[
            filtered_df["Project_Name"].astype(str).str.lower().str.contains(search_text, na=False)
            | filtered_df["Project_ID"].astype(str).str.lower().str.contains(search_text, na=False)
            | filtered_df["State"].astype(str).str.lower().str.contains(search_text, na=False)
        ]

    st.write(t("found_proj", count=len(filtered_df)))

    if filtered_df.empty:
        st.warning(t("no_match"))
    else:
        for index, row in filtered_df.reset_index(drop=True).iterrows():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

                with col1:
                    st.markdown(f"**{row['Project_Name']}**")
                    st.caption(f"{row['Project_ID']} • {row['State']}")

                with col2:
                    st.write(t("phys_progress_hdr"))
                    st.write(f"**{row['Physical_Progress_Percent']:.1f}%**")

                with col3:
                    st.write(t("risk"))
                    st.write(f"**{row['Risk_Level']}**")

                with col4:
                    search_key = f"search_details_{row['Project_ID']}_{index}"

                    if st.button(t("details_btn"), key=search_key):
                        st.session_state["search_selected_project"] = row["Project_ID"]

            if st.session_state.get("search_selected_project") == row["Project_ID"]:
                show_project_details(row)

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption(t("footer"))