# Global Cyberattack Pattern Analysis — Dashboard
# Author: Raghad

import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------- Page Setup -----------------------------
st.set_page_config(
    page_title="Global Cyberattack Pattern Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Theme Toggle -----------------------------
dark_mode = st.toggle("🌙 Dark Mode", value=True)

def theme_css(dark=True):
    if dark:
        return """
        <style>
        body, .stApp {
            background-color: #0b1220;
            color: #e5e7eb;
        }
        h1, h2, h3, h4 {
            color: #f9fafb;
        }
        .hero {
            background: linear-gradient(135deg, #020617, #020617);
            box-shadow: 0 30px 60px rgba(0,0,0,.45);
            border-radius: 16px;
        }
        .e-card {
            background: #111827;
            border-radius: 14px;
            box-shadow: 0 18px 40px rgba(0,0,0,.45);
            transition: all 0.35s ease;
        }
        .e-card:hover {
            transform: translateY(-6px) scale(1.015);
        }
        .stDataFrame {
            background-color: #020617;
        }
        </style>
        """
    else:
        return """
        <style>
        body, .stApp {
            background-color: #ffffff;
            color: #0f172a;
        }
        h1, h2, h3, h4 {
            color: #020617;
        }
        .hero {
            background: linear-gradient(135deg, #0f172a, #020617);
            box-shadow: 0 18px 40px rgba(0,0,0,.18);
            border-radius: 16px;
        }
        .e-card {
            background: #ffffff;
            border-radius: 14px;
            box-shadow: 0 12px 26px rgba(0,0,0,.12);
            transition: all 0.3s ease;
        }
        .e-card:hover {
            transform: translateY(-4px) scale(1.01);
        }
        </style>
        """

st.markdown(theme_css(dark_mode), unsafe_allow_html=True)

# ----------------------------- Data Load -----------------------------
DATA_PATH = Path("data/kev_clean.csv")
df = pd.read_csv(DATA_PATH)

# ----------------------------- Sidebar -----------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select an analysis module",
    [
        "EDA Overview",
        "Modeling Results",
        "Clustering Insights",
        "Association Rules",
        "Trends & Forecast",
    ],
)

# ----------------------------- Hero Section -----------------------------
st.markdown(
    """
    <div class="hero" style="padding:30px;">
        <h1>Global Cyberattack Pattern Analysis</h1>
        <p>
        Interactive analytical dashboard built on <b>CISA Known Exploited Vulnerabilities (KEV)</b> data.
        It presents exploratory analysis, machine learning results, clustering insights,
        association rules, and long-term temporal trends.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------- EDA -----------------------------
if section == "EDA Overview":

    st.header("Exploratory Data Analysis")

    col1, col2, col3 = st.columns(3)

    col1.markdown(
        f"""
        <div class="e-card" style="padding:20px">
            <h3>Total CVEs</h3>
            <h2>{df['cve_id'].nunique()}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col2.markdown(
        f"""
        <div class="e-card" style="padding:20px">
            <h3>Unique Vendors</h3>
            <h2>{df['vendor'].nunique()}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col3.markdown(
        f"""
        <div class="e-card" style="padding:20px">
            <h3>Unique Products</h3>
            <h2>{df['product'].nunique()}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    df["cve_year"].value_counts().sort_index().plot(kind="bar", ax=ax)
    ax.set_title("Distribution by CVE Year")
    st.pyplot(fig)

# ----------------------------- Modeling -----------------------------
elif section == "Modeling Results":

    st.header("Machine Learning Results")

    results = pd.DataFrame(
        {
            "Model": ["Random Forest", "Gradient Boosting", "SVM"],
            "Accuracy": [0.99, 1.00, 0.97],
            "Macro-F1": [0.99, 1.00, 0.96],
        }
    )

    st.dataframe(results, use_container_width=True)

    st.info(
        "All models were trained and evaluated in the modeling.ipynb notebook. "
        "The dashboard displays final evaluation metrics only."
    )

# ----------------------------- Footer -----------------------------
st.markdown(
    """
    <hr>
    <center>
    © 2025 Raghad Ali · Cybersecurity & Data Analytics
    </center>
    """,
    unsafe_allow_html=True,
)
