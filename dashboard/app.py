# Global Cyberattack Pattern Analysis — Dashboard
# Author: Raghad

import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------- Page Setup -----------------------------
st.set_page_config(
    page_title="Global Cyberattack Pattern Analysis",
    page_icon="🌐",
    layout="wide"
)

# ----------------------------- Styling -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, Segoe UI, Roboto;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 32px;
    color: white;
}

/* KPI Cards */
.e-card {
    padding: 20px;
    border-radius: 14px;
    background: white;
    border: 1px solid rgba(0,0,0,.05);
    box-shadow: 0 8px 18px rgba(0,0,0,.05);
    transition: transform .15s ease;
}
.e-card:hover {
    transform: translateY(-3px);
}

.kpi-title {
    font-size: .8rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: .04em;
}
.kpi-value {
    font-size: 1.7rem;
    font-weight: 700;
    color: #0f172a;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------- Hero Header -----------------------------
st.markdown("""
<div class="hero">
    <h2>Global Cyberattack Pattern Analysis</h2>
    <p style="opacity:.9; max-width: 780px;">
        Interactive analytical dashboard built on CISA Known Exploited Vulnerabilities (KEV) data.
        The dashboard presents exploratory analysis, machine learning results, clustering insights,
        association rules, and long-term temporal trends.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------- Sidebar -----------------------------
st.sidebar.markdown("## Navigation")
st.sidebar.caption("Select an analysis module")

menu = st.sidebar.radio(
    "",
    [
        "EDA Overview",
        "Modeling Results",
        "Clustering Insights",
        "Association Rules",
        "Trends & Forecast"
    ]
)

# ----------------------------- Paths -----------------------------
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT.parent / "data" / "cisa_kev.csv"
FIGURES = ROOT.parent / "figures"

@st.cache_data
def load_data(path):
    return pd.read_csv(path, low_memory=False)

df = load_data(DATA_PATH)

# ----------------------------- Helpers -----------------------------
def kpi_card(title, value):
    st.markdown(f"""
    <div class="e-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def show_figure(filename, caption, description=None):
    if description:
        st.caption(description)
    path = FIGURES / filename
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(f"`{filename}` not generated yet (run the notebook).")

# ============================= EDA =============================
if menu == "EDA Overview":
    st.subheader("Exploratory Data Analysis")
    st.caption("High-level overview of vulnerability volume, vendors, and products.")

    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total CVEs", f"{len(df):,}")
    with c2: kpi_card("Unique Vendors", df["vendorProject"].nunique())
    with c3: kpi_card("Unique Products", df["product"].nunique())

    st.subheader("CVE Year Distribution")
    show_figure(
        "cve_year_distribution.png",
        "Distribution of CVEs by Year",
        "Illustrates the evolution of disclosed vulnerabilities over time."
    )

    st.subheader("Monthly Distribution")
    show_figure(
        "monthly_distribution.png",
        "Monthly Distribution of CVEs",
        "Reveals temporal and seasonal disclosure patterns."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ransomware Association")
        show_figure(
            "ransomware_flag.png",
            "Ransomware-Linked Vulnerabilities",
            "Indicates whether vulnerabilities are associated with known ransomware campaigns."
        )
    with col2:
        st.subheader("Top Vendors")
        show_figure(
            "top_vendors.png",
            "Most Affected Vendors",
            "Vendors most frequently appearing in the KEV catalogue."
        )

    st.subheader("Top Products")
    show_figure(
        "top_products.png",
        "Most Affected Products",
        "Products with the highest number of critical vulnerabilities."
    )

# ============================= MODELING =============================
elif menu == "Modeling Results":
    st.subheader("Machine Learning Results")
    st.caption("Supervised models trained to classify vulnerability characteristics.")

    model_scores = pd.DataFrame({
        "Model": ["Random Forest", "Gradient Boosting", "SVM"],
        "Accuracy": [0.99, 1.00, 0.97],
        "Macro-F1": [0.99, 1.00, 0.96]
    })
    st.dataframe(model_scores, use_container_width=True)

    st.info(
        "All models were trained and evaluated in the `modeling.ipynb` notebook. "
        "The dashboard displays final evaluation metrics only."
    )

# ============================= CLUSTERING =============================
elif menu == "Clustering Insights":
    st.subheader("Clustering Insights")
    st.caption("Unsupervised clustering to identify similarity patterns across vendors and time.")

    col1, col2 = st.columns(2)
    with col1:
        show_figure(
            "sb_top_vendors.png",
            "Vendor Clusters",
            "Similarity-based clustering of vendors."
        )
    with col2:
        show_figure(
            "sb_year_added.png",
            "Clusters by Year Added",
            "Temporal distribution of vulnerabilities within clusters."
        )

# ============================= ASSOCIATION RULES =============================
elif menu == "Association Rules":
    st.subheader("Association Rule Mining")
    st.caption("Frequent co-occurrence patterns across vendors and months.")

    col1, col2 = st.columns(2)
    with col1:
        show_figure(
            "vendor_month_top20.png",
            "Vendor–Month Heatmap (Top 20)",
            "Monthly vulnerability concentration for top vendors."
        )
    with col2:
        show_figure(
            "vendor_month_top20_pct.png",
            "Vendor–Month Heatmap (%)",
            "Normalized monthly distribution by vendor."
        )

# ============================= TRENDS =============================
elif menu == "Trends & Forecast":
    st.subheader("Temporal Trends")
    st.caption("Long-term evolution of vulnerability disclosures.")

    show_figure(
        "timeline_by_month.png",
        "Timeline of CVEs by Month",
        "Overall vulnerability disclosure timeline."
    )

    col1, col2 = st.columns(2)
    with col1:
        show_figure(
            "trend_by_year.png",
            "Yearly Trend of CVEs",
            "Annual growth trend of vulnerabilities."
        )
    with col2:
        show_figure(
            "trend_boxplot_year.png",
            "Distribution of CVEs per Year",
            "Yearly variability in CVE counts."
        )

    st.subheader("Forecast (Planned)")
    st.caption("Time-series forecasting using Prophet or LSTM will be added in a future release.")


st.markdown("""
<hr style="margin-top: 50px; margin-bottom: 15px; border: none; border-top: 1px solid #e5e7eb;">
<p style="
    text-align: center;
    color: #6b7280;
    font-size: 0.85rem;
">
    © 2025 Raghad Ali · Cybersecurity & Data Analytics
</p>
""", unsafe_allow_html=True)
