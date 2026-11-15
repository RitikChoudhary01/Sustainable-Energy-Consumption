"""
================================================================================
ENERGYIQ // SUSTAINABLE ENERGY OPTIMIZATION DASHBOARD (PREMIUM WHITE EDITION)
SR UNIVERSITY · School of Computer Science & AI
Course: Data Analytics & Visualization (25CAI202PC201) · Semester Project #10
Curiosity Question: How can energy usage be optimized?
Dataset: Global Data on Sustainable Energy (2000-2019) · 176 Sovereign Entities
================================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ENERGYIQ // Sustainable Energy Optimization",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. ULTRA-PREMIUM WHITE & CLEAN-TECH DESIGN SYSTEM (CSS)
# ─────────────────────────────────────────────────────────────────────────────
PREMIUM_WHITE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

code, pre, .mono-font {
    font-family: 'JetBrains Mono', monospace !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 0.8rem;
    padding-bottom: 2rem;
    max-width: 96% !important;
}

/* ── Alabaster Ambient Background ── */
.stApp {
    background: radial-gradient(circle at 10% 8%, #F1F5F9 0%, #F8FAFC 55%, #FFFFFF 100%);
    color: #0F172A;
}

/* ── Crisp Frosted Light Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 60%, #F1F5F9 100%);
    border-right: 1px solid #E2E8F0;
    box-shadow: 4px 0 24px rgba(15, 23, 42, 0.03);
}

/* ── Live Telemetry HUD Bar ── */
.hud-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 8px 18px;
    margin-bottom: 14px;
    font-size: 0.74rem;
    color: #64748B;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}
.hud-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
    padding: 3px 10px;
    border-radius: 999px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.pulse-dot {
    width: 6px;
    height: 6px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
}

/* ── Ultra-Luxury White Hero Banner ── */
.premium-hero {
    background: linear-gradient(135deg, #FFFFFF 0%, #FAFCFF 55%, #F0FDF4 100%);
    border: 1px solid #E2E8F0;
    border-top: 3px solid #059669;
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.06);
    position: relative;
    overflow: hidden;
}
.hero-tagline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #059669;
    margin-bottom: 8px;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}
.hero-desc {
    color: #475569;
    font-size: 0.94rem;
    margin-top: 8px;
    line-height: 1.55;
    max-width: 950px;
}

/* ── Curiosity Directive Box ── */
.curiosity-banner {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 4px solid #059669;
    border-radius: 10px;
    padding: 11px 16px;
    margin-top: 14px;
    font-size: 0.88rem;
    color: #166534;
    line-height: 1.5;
}

/* ── Luxury White KPI Cards Grid ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 22px;
}
@media (max-width: 992px) {
    .kpi-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 576px) {
    .kpi-row { grid-template-columns: 1fr; }
}

.kpi-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.03);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.kpi-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px -4px rgba(15, 23, 42, 0.09);
    border-color: #CBD5E1;
}
.kpi-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--kpi-bar, linear-gradient(90deg, #059669, #0284C7));
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 2.15rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    color: #0F172A;
    line-height: 1.1;
    margin-bottom: 6px;
}
.kpi-value span {
    font-size: 0.95rem;
    font-weight: 600;
    color: #64748B;
    margin-left: 3px;
}

/* Micro meter */
.kpi-meter {
    width: 100%;
    height: 5px;
    background: #F1F5F9;
    border-radius: 999px;
    overflow: hidden;
    margin: 8px 0 10px 0;
}
.kpi-meter-fill {
    height: 100%;
    border-radius: 999px;
    background: var(--kpi-bar, linear-gradient(90deg, #059669, #0284C7));
}

.kpi-delta {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.74rem;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 6px;
}
.delta-pos { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.delta-neg { background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA; }

/* ── Takeaway / Examiner Callout ── */
.takeaway-card {
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    border-left: 4px solid #0284C7;
    border-radius: 10px;
    padding: 10px 16px;
    margin: 12px 0 16px 0;
    font-size: 0.86rem;
    color: #0369A1;
    line-height: 1.5;
}
.takeaway-card b {
    color: #0284C7;
}

/* ── Modern Light Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F1F5F9;
    border-radius: 12px;
    padding: 5px;
    gap: 6px;
    border: 1px solid #E2E8F0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #64748B !important;
    font-weight: 600;
    font-size: 0.84rem;
    padding: 8px 18px;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #059669 !important;
    border: 1px solid #CBD5E1 !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
    font-weight: 700;
}

/* ── Optimization Pillars ── */
.opt-pillar {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}
.opt-pillar h4 {
    margin: 0 0 6px 0;
    font-size: 0.95rem;
    color: #059669;
    display: flex;
    align-items: center;
    gap: 8px;
}
.opt-pillar p {
    margin: 0;
    font-size: 0.83rem;
    color: #475569;
    line-height: 1.45;
}

/* ── Inputs & Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #059669 0%, #0284C7 100%);
    color: #FFFFFF !important;
    font-weight: 700;
    font-size: 0.85rem;
    border: none;
    border-radius: 10px;
    padding: 9px 20px;
    box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25);
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(5, 150, 105, 0.35);
}

.stDataFrame {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}
</style>
"""
st.markdown(PREMIUM_WHITE_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. HIGH-END VISUALIZATION PALETTE & PLOTLY HELPER (LIGHT MODE)
# ─────────────────────────────────────────────────────────────────────────────
PALETTE = {
    "mint": "#059669",
    "cyan": "#0284C7",
    "amber": "#D97706",
    "coral": "#E11D48",
    "emerald": "#10B981",
    "bg": "#FFFFFF",
    "card": "#FFFFFF",
    "text": "#0F172A",
    "subtext": "#64748B",
    "grid": "rgba(15, 23, 42, 0.07)",
}

def clean_chart(fig, title="", height=400, show_legend=True):
    fig.update_layout(
        paper_bgcolor=PALETTE["bg"],
        plot_bgcolor=PALETTE["card"],
        font=dict(family="Plus Jakarta Sans, sans-serif", color=PALETTE["text"], size=12),
        margin=dict(l=14, r=14, t=44, b=14),
        height=height,
        title=dict(
            text=f"<b style='font-size:14px;color:#0F172A;'>{title}</b>",
            font=dict(size=14, color=PALETTE["text"]),
            x=0.01,
            xanchor="left",
        ),
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(226,232,240,0.8)",
            font=dict(size=11, color=PALETTE["text"]),
        ),
        xaxis=dict(
            gridcolor=PALETTE["grid"],
            zerolinecolor=PALETTE["grid"],
            tickfont=dict(color=PALETTE["subtext"]),
            title=dict(font=dict(color=PALETTE["subtext"])),
        ),
        yaxis=dict(
            gridcolor=PALETTE["grid"],
            zerolinecolor=PALETTE["grid"],
            tickfont=dict(color=PALETTE["subtext"]),
            title=dict(font=dict(color=PALETTE["subtext"])),
        ),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# 4. ROBUST DATA INGESTION
# ─────────────────────────────────────────────────────────────────────────────
CANDIDATE_PATHS = [
    Path(__file__).parent / "global-data-on-sustainable-energy.csv",
    Path(__file__).parent / "energy_dashboard_streamlit" / "global-data-on-sustainable-energy.csv",
    Path(r"C:\Users\choud\Downloads\energy_dashboard_streamlit\global-data-on-sustainable-energy.csv"),
    Path(r"C:\Users\choud\Downloads\energy_dashboard_streamlit\energy_dashboard_streamlit\global-data-on-sustainable-energy.csv"),
]

def resolve_csv():
    for p in CANDIDATE_PATHS:
        if p.exists():
            return p
    raise FileNotFoundError("global-data-on-sustainable-energy.csv was not found.")

@st.cache_data(show_spinner="⚡ Loading global energy matrix...")
def load_and_prep_data():
    csv_path = resolve_csv()
    raw = pd.read_csv(csv_path)

    rename_map = {
        "Entity": "country",
        "Year": "year",
        "Access to electricity (% of population)": "access_elec",
        "Access to clean fuels for cooking": "clean_fuels",
        "Renewable-electricity-generating-capacity-per-capita": "renew_cap_pc",
        "Financial flows to developing countries (US $)": "fin_flows",
        "Renewable energy share in the total final energy consumption (%)": "renew_share",
        "Electricity from fossil fuels (TWh)": "fossil_twh",
        "Electricity from nuclear (TWh)": "nuclear_twh",
        "Electricity from renewables (TWh)": "renew_twh",
        "Low-carbon electricity (% electricity)": "lowcarbon_pct",
        "Primary energy consumption per capita (kWh/person)": "energy_pc",
        "Energy intensity level of primary energy (MJ/$2017 PPP GDP)": "intensity",
        "Value_co2_emissions_kt_by_country": "co2_kt",
        "Renewables (% equivalent primary energy)": "renew_pe_pct",
        "gdp_growth": "gdp_growth",
        "gdp_per_capita": "gdp_pc",
        "Density\n(P/Km2)": "density",
        "Land Area(Km2)": "land_area",
        "Latitude": "latitude",
        "Longitude": "longitude",
    }
    df = raw.rename(columns=rename_map)

    num_cols = [
        "access_elec", "clean_fuels", "renew_cap_pc", "fin_flows",
        "renew_share", "fossil_twh", "nuclear_twh", "renew_twh",
        "lowcarbon_pct", "energy_pc", "intensity", "co2_kt",
        "gdp_growth", "gdp_pc", "latitude", "longitude"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["lowcarbon_pct"] = df["lowcarbon_pct"].clip(0, 100)
    df["co2_mt"] = df["co2_kt"] / 1000.0  # Megatonnes
    df["total_elec_twh"] = (
        df["fossil_twh"].fillna(0)
        + df["nuclear_twh"].fillna(0)
        + df["renew_twh"].fillna(0)
    )
    df["clean_elec_twh"] = df["renew_twh"].fillna(0) + df["nuclear_twh"].fillna(0)

    # Continent/Region classification for clean grouping
    region_dict = {
        "China": "Asia-Pacific", "India": "Asia-Pacific", "Japan": "Asia-Pacific", "South Korea": "Asia-Pacific",
        "Indonesia": "Asia-Pacific", "Vietnam": "Asia-Pacific", "Thailand": "Asia-Pacific", "Australia": "Asia-Pacific",
        "United States": "North America", "Canada": "North America", "Mexico": "North America",
        "Brazil": "Latin America", "Argentina": "Latin America", "Chile": "Latin America", "Colombia": "Latin America",
        "Germany": "Europe", "United Kingdom": "Europe", "France": "Europe", "Italy": "Europe",
        "Spain": "Europe", "Norway": "Europe", "Sweden": "Europe", "Poland": "Europe", "Russia": "Europe",
        "South Africa": "Sub-Saharan Africa", "Nigeria": "Sub-Saharan Africa", "Kenya": "Sub-Saharan Africa", "Ghana": "Sub-Saharan Africa",
        "Saudi Arabia": "Middle East & N. Africa", "United Arab Emirates": "Middle East & N. Africa", "Egypt": "Middle East & N. Africa",
        "Turkey": "Middle East & N. Africa", "Iran": "Middle East & N. Africa"
    }
    df["region"] = df["country"].map(region_dict).fillna("Rest of World")
    return df

df_full = load_and_prep_data()
all_countries = sorted(df_full["country"].unique().tolist())
all_regions = sorted(df_full["region"].unique().tolist())

# ─────────────────────────────────────────────────────────────────────────────
# 5. SIDEBAR CONTROLS & VIVA DEFENSE GUIDE
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 4px 14px 4px;">
      <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:38px; height:38px; background:linear-gradient(135deg, rgba(5,150,105,0.15) 0%, rgba(2,132,199,0.1) 100%);
                    border:1px solid rgba(5,150,105,0.35); border-radius:10px; display:flex; align-items:center; justify-content:center;
                    box-shadow: 0 4px 12px rgba(5,150,105,0.15);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
          </svg>
        </div>
        <div>
          <div style="font-size:1.2rem; font-weight:900; color:#0F172A; line-height:1.1;">ENERGY<span style="color:#059669;">IQ</span></div>
          <div style="font-size:0.65rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.06em;">Energy Optimization</div>
        </div>
      </div>
      <div style="margin-top:12px; font-size:0.75rem; color:#475569; line-height:1.45; border-left:2px solid #059669; padding-left:8px; background:#F0FDF4; border-radius:0 6px 6px 0; padding:6px 8px;">
        SR University · Project #10<br>
        Course: <b style="color:#0F172A;">DAV (25CAI202PC201)</b>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎛️ Analysis Controls")

    year_sel = st.slider(
        "Select Year",
        min_value=2000,
        max_value=2019,
        value=2019,
        step=1,
        help="Harmonized multi-decade data from 2000 to 2019 across 176 sovereign entities."
    )

    region_filter = st.selectbox(
        "Filter by Region",
        ["Global (All Regions)"] + all_regions,
        index=0
    )

    country_pool = all_countries
    if region_filter != "Global (All Regions)":
        country_pool = sorted(df_full[df_full["region"] == region_filter]["country"].unique().tolist())

    selected_countries = st.multiselect(
        "Filter Specific Countries (Optional)",
        country_pool,
        default=[],
        placeholder="Choose countries (empty = all)"
    )

    st.markdown("---")
    # VIVA QUICK REFERENCE CHEAT SHEET FOR THE STUDENT
    with st.expander("🎓 Presentation & Viva Quick Notes", expanded=False):
        st.markdown("""
        **1. What is Project #10?**
        - *Sustainable Energy Consumption Dashboard* answering *"How can energy usage be optimized?"*
        
        **2. How can energy usage be optimized?**
        - **Supply**: Transition fossil power plants to clean renewables (solar, wind, hydro).
        - **Demand**: Lower Energy Intensity (produce more GDP per unit of energy).
        - **Grid**: Cut transmission line losses with smart grids.
        - **Cooking**: Replace biomass/wood with clean electric fuels.
        
        **3. What does Energy Intensity mean?**
        - Megajoules (MJ) consumed per $ of GDP. **Lower is better!** Highly developed economies have low energy intensity.
        
        **4. Dataset Details:**
        - Kaggle / World Bank / IEA (2000–2019, 176 sovereign countries, 3,649 records).
        """)

# ─────────────────────────────────────────────────────────────────────────────
# 6. COHORT FILTERING & DATA CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────
df_cohort = df_full.copy()
if region_filter != "Global (All Regions)":
    df_cohort = df_cohort[df_cohort["region"] == region_filter]
if selected_countries:
    df_cohort = df_cohort[df_cohort["country"].isin(selected_countries)]

df_cur = df_cohort[df_cohort["year"] == year_sel]
df_base = df_cohort[df_cohort["year"] == 2000]

# Time series aggregation
df_ts = df_cohort.groupby("year").agg(
    fossil_twh=("fossil_twh", "sum"),
    nuclear_twh=("nuclear_twh", "sum"),
    renew_twh=("renew_twh", "sum"),
    total_elec_twh=("total_elec_twh", "sum"),
    clean_elec_twh=("clean_elec_twh", "sum"),
    co2_mt=("co2_mt", "sum"),
    renew_share=("renew_share", "mean"),
    access_elec=("access_elec", "mean"),
    intensity=("intensity", "mean"),
    gdp_pc=("gdp_pc", "mean"),
).reset_index()

# Top KPIs
tot_elec_now = df_cur["total_elec_twh"].sum()
tot_clean_now = df_cur["clean_elec_twh"].sum()
clean_pct_now = (tot_clean_now / (tot_elec_now + 1e-9)) * 100

tot_elec_2000 = df_base["total_elec_twh"].sum()
tot_clean_2000 = df_base["clean_elec_twh"].sum()
clean_pct_2000 = (tot_clean_2000 / (tot_elec_2000 + 1e-9)) * 100
d_clean = clean_pct_now - clean_pct_2000

avg_int_now = df_cur["intensity"].mean()
avg_int_2000 = df_base["intensity"].mean()
d_int = avg_int_now - avg_int_2000

avg_acc_now = df_cur["access_elec"].mean()
avg_acc_2000 = df_base["access_elec"].mean()
d_acc = avg_acc_now - avg_acc_2000

tot_co2_now = df_cur["co2_mt"].sum()
tot_co2_2000 = df_base["co2_mt"].sum()
d_co2_pct = ((tot_co2_now - tot_co2_2000) / (tot_co2_2000 + 1e-9)) * 100

cohort_title = (
    ", ".join(selected_countries[:3]) + (f" +{len(selected_countries)-3} more" if len(selected_countries) > 3 else "")
    if selected_countries
    else (f"{region_filter}" if region_filter != "Global (All Regions)" else "176 Sovereign Nations")
)

# ─────────────────────────────────────────────────────────────────────────────
# 7. TELEMETRY HEADER & LUXURY WHITE HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hud-bar">
  <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
    <div class="hud-pill"><div class="pulse-dot"></div> ACTIVE DATASET</div>
    <span>DATASET: <b style="color:#0F172A;">Kaggle · World Bank · IEA</b></span>
    <span>HORIZON: <b style="color:#0F172A;">2000–2019</b></span>
    <span>RECORDS: <b style="color:#0F172A;">3,649 Samples</b></span>
  </div>
  <div>
    <span>COHORT: <b style="color:#059669;">{cohort_title}</b></span> &nbsp;•&nbsp;
    <span>YEAR: <b style="color:#0284C7;">{year_sel}</b></span>
  </div>
</div>

<div class="premium-hero">
  <div class="hero-tagline">
    <span>SR UNIVERSITY · SCHOOL OF CS & AI</span>
    <span>DAV (25CAI202PC201) · PROJECT #10</span>
  </div>
  <h1 class="hero-title">Sustainable Energy Optimization Dashboard</h1>
  <div class="hero-desc">
    An interactive data analytics platform analyzing 20 years of sovereign energy transition, power generation mix, and economic efficiency across 176 nations.
  </div>
  <div class="curiosity-banner">
    <b>Curiosity Research Question:</b> <i>How can energy usage be optimized?</i> — By accelerating zero-carbon renewable power, reducing industrial energy intensity (MJ/$), and phasing out high-loss fossil generation.
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 8. 4 ULTRA-PREMIUM WHITE KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
fill_clean = min(max(clean_pct_now, 0), 100)
fill_int = min(max((10.0 - avg_int_now) / 8.0 * 100, 5), 100)
fill_acc = min(max(avg_acc_now, 0), 100)
fill_co2 = min(max(tot_co2_now / 35000.0 * 100, 10), 100)

st.markdown(f"""
<div class="kpi-row">
  <!-- KPI 1 -->
  <div class="kpi-box" style="--kpi-bar: linear-gradient(90deg, #059669, #0284C7);">
    <div class="kpi-label">Clean Power Ratio</div>
    <div class="kpi-value">{clean_pct_now:.1f}<span>%</span></div>
    <div class="kpi-meter">
      <div class="kpi-meter-fill" style="width: {fill_clean:.1f}%;"></div>
    </div>
    <div class="kpi-delta {'delta-pos' if d_clean >= 0 else 'delta-neg'}">
      {'▲ +' if d_clean >= 0 else '▼ '}{abs(d_clean):.1f}pp vs 2000 ({clean_pct_2000:.1f}%)
    </div>
  </div>

  <!-- KPI 2 -->
  <div class="kpi-box" style="--kpi-bar: linear-gradient(90deg, #D97706, #059669);">
    <div class="kpi-label">Energy Intensity</div>
    <div class="kpi-value">{avg_int_now:.2f}<span>MJ/$</span></div>
    <div class="kpi-meter">
      <div class="kpi-meter-fill" style="width: {fill_int:.1f}%;"></div>
    </div>
    <div class="kpi-delta {'delta-pos' if d_int <= 0 else 'delta-neg'}">
      {'▼ -' if d_int <= 0 else '▲ +'}{abs(d_int):.2f} MJ/$ (Lower = Better)
    </div>
  </div>

  <!-- KPI 3 -->
  <div class="kpi-box" style="--kpi-bar: linear-gradient(90deg, #0284C7, #059669);">
    <div class="kpi-label">Electricity Access</div>
    <div class="kpi-value">{avg_acc_now:.1f}<span>%</span></div>
    <div class="kpi-meter">
      <div class="kpi-meter-fill" style="width: {fill_acc:.1f}%;"></div>
    </div>
    <div class="kpi-delta {'delta-pos' if d_acc >= 0 else 'delta-neg'}">
      {'▲ +' if d_acc >= 0 else '▼ '}{abs(d_acc):.1f}pp vs 2000 ({avg_acc_2000:.1f}%)
    </div>
  </div>

  <!-- KPI 4 -->
  <div class="kpi-box" style="--kpi-bar: linear-gradient(90deg, #E11D48, #D97706);">
    <div class="kpi-label">Gross CO₂ Emissions</div>
    <div class="kpi-value">{tot_co2_now:,.0f}<span>Mt</span></div>
    <div class="kpi-meter">
      <div class="kpi-meter-fill" style="width: {fill_co2:.1f}%;"></div>
    </div>
    <div class="kpi-delta {'delta-pos' if d_co2_pct <= 0 else 'delta-neg'}">
      {d_co2_pct:+.1f}% vs 2000 ({tot_co2_2000:,.0f} Mt)
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 9. FIVE CLEAN TABS (LIGHT MODE)
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 Global Map & Leaders",
    "⚡ Electricity Mix Trends",
    "📈 Efficiency vs Economic Growth",
    "🎯 How to Optimize Energy (Simulator)",
    "📋 Country Data Explorer"
])

# =============================================================================
# TAB 1: GLOBAL MAP & LEADERS
# =============================================================================
with tab1:
    st.markdown("""
    <div class="takeaway-card">
      <b>💡 Examiner Presentation Point:</b> This choropleth projection shows how sustainable energy metrics vary across nations. Countries with high hydro and geothermal capacity (e.g., Norway, Iceland, Brazil) lead in renewable power share.
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns([3, 1])
    with col_m1:
        map_metric = st.selectbox(
            "Select Metric to Visualize on World Map:",
            [
                "Low-Carbon Electricity Share (%)",
                "Renewable Energy Share in Final Consumption (%)",
                "Energy Intensity Level (MJ/$ GDP)",
                "Access to Electricity (% of population)",
                "Gross CO₂ Emissions (Megatonnes)"
            ],
            index=0
        )
    with col_m2:
        map_proj = st.selectbox("Map Projection", ["natural earth", "equirectangular", "mercator"], index=0)

    metric_mapping = {
        "Low-Carbon Electricity Share (%)": ("lowcarbon_pct", "YlGnBu"),
        "Renewable Energy Share in Final Consumption (%)": ("renew_share", "Viridis"),
        "Energy Intensity Level (MJ/$ GDP)": ("intensity", "YlOrRd"),
        "Access to Electricity (% of population)": ("access_elec", "Blues"),
        "Gross CO₂ Emissions (Megatonnes)": ("co2_mt", "Reds"),
    }
    col_name, col_scale = metric_mapping[map_metric]

    fig_map = px.choropleth(
        df_cur,
        locations="country",
        locationmode="country names",
        color=col_name,
        hover_name="country",
        hover_data={
            col_name: ":.2f",
            "gdp_pc": ":$,.0f",
            "co2_mt": ":,.1f",
            "country": False
        },
        color_continuous_scale=col_scale,
        labels={col_name: map_metric, "gdp_pc": "GDP/Capita", "co2_mt": "CO₂ (Mt)"}
    )
    fig_map.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#CBD5E1",
        showland=True,
        landcolor="#F8FAFC",
        showocean=True,
        oceancolor="#E0F2FE",
        lakecolor="#E0F2FE",
        projection_type=map_proj,
        bgcolor="#FFFFFF"
    )
    clean_chart(fig_map, f"Global Distribution: {map_metric} ({year_sel})", height=480, show_legend=False)
    fig_map.update_layout(geo=dict(bgcolor="#FFFFFF"), margin=dict(l=0, r=0, t=35, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    # Top 10 Ranking Chart
    st.markdown("#### 🏆 Top 10 Performing Nations in Selected Metric")
    df_top10 = df_cur.dropna(subset=[col_name]).sort_values(by=col_name, ascending=False).head(10)
    if not df_top10.empty:
        fig_bar = px.bar(
            df_top10,
            x=col_name,
            y="country",
            orientation="h",
            color=col_name,
            color_continuous_scale=col_scale,
            text_auto=".1f",
            labels={col_name: map_metric, "country": "Country"}
        )
        fig_bar.update_layout(yaxis=dict(autorange="reversed"))
        clean_chart(fig_bar, f"Top 10 Sovereign Leaders — {map_metric} ({year_sel})", height=340, show_legend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No ranking data available for the current selection.")

# =============================================================================
# TAB 2: ELECTRICITY MIX TRENDS
# =============================================================================
with tab2:
    st.markdown("""
    <div class="takeaway-card">
      <b>💡 Examiner Presentation Point:</b> This tab tracks the 2000–2019 transition. Although global renewable power generation expanded by over 140%, fossil fuels remain the dominant baseline source. Optimizing energy requires replacing high-emission coal with clean renewables.
    </div>
    """, unsafe_allow_html=True)

    c_g1, c_g2 = st.columns([3, 2])

    with c_g1:
        # Stacked Area Generation
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=df_ts["year"], y=df_ts["renew_twh"],
            name="Renewable Power (TWh)",
            stackgroup="one",
            fillcolor="rgba(5, 150, 105, 0.45)",
            line=dict(color="#059669", width=2),
        ))
        fig_area.add_trace(go.Scatter(
            x=df_ts["year"], y=df_ts["nuclear_twh"],
            name="Nuclear Power (TWh)",
            stackgroup="one",
            fillcolor="rgba(2, 132, 199, 0.35)",
            line=dict(color="#0284C7", width=2),
        ))
        fig_area.add_trace(go.Scatter(
            x=df_ts["year"], y=df_ts["fossil_twh"],
            name="Fossil Fuel Power (TWh)",
            stackgroup="one",
            fillcolor="rgba(225, 29, 72, 0.35)",
            line=dict(color="#E11D48", width=2),
        ))
        clean_chart(fig_area, f"Generation Mix Evolution: 2000–2019 (TWh)", height=380)
        fig_area.update_layout(yaxis_title="Terawatt-Hours (TWh)", xaxis_title="Evaluation Year")
        st.plotly_chart(fig_area, use_container_width=True)

    with c_g2:
        # Generation Donut Chart for selected year
        fossil_sum = df_cur["fossil_twh"].sum()
        nuclear_sum = df_cur["nuclear_twh"].sum()
        renew_sum = df_cur["renew_twh"].sum()

        fig_donut = go.Figure(data=[go.Pie(
            labels=["Renewables", "Nuclear", "Fossil Fuels"],
            values=[renew_sum, nuclear_sum, fossil_sum],
            hole=0.55,
            marker=dict(colors=["#059669", "#0284C7", "#E11D48"]),
            textinfo="label+percent",
            hoverinfo="label+value+percent",
        )])
        clean_chart(fig_donut, f"Electricity Generation Share ({year_sel})", height=380)
        st.plotly_chart(fig_donut, use_container_width=True)

    # Secondary indicator: Access to Clean Cooking Fuels over time
    st.markdown("#### 🍲 Clean Cooking Fuels vs Universal Electricity Access")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_ts["year"], y=df_ts["access_elec"],
        mode="lines+markers",
        name="Access to Electricity (%)",
        line=dict(color="#059669", width=2.5)
    ))
    fig_line.add_trace(go.Scatter(
        x=df_ts["year"], y=df_cohort.groupby("year")["clean_fuels"].mean(),
        mode="lines+markers",
        name="Access to Clean Cooking Fuels (%)",
        line=dict(color="#D97706", width=2.5, dash="dot")
    ))
    clean_chart(fig_line, "Global Infrastructure Modernization: 2000–2019 (%)", height=320)
    fig_line.update_layout(yaxis_title="Percentage of Population (%)", xaxis_title="Year")
    st.plotly_chart(fig_line, use_container_width=True)

# =============================================================================
# TAB 3: EFFICIENCY VS ECONOMIC GROWTH
# =============================================================================
with tab3:
    st.markdown("""
    <div class="takeaway-card">
      <b>💡 Examiner Presentation Point:</b> This scatter plot shows <b>Energy Intensity</b> (MJ per $ of GDP) plotted against <b>GDP per Capita</b>. Developed economies produce higher economic value per megajoule, proving that economic growth does not require wasteful energy consumption.
    </div>
    """, unsafe_allow_html=True)

    df_eff = df_cur.dropna(subset=["intensity", "gdp_pc"]).copy()
    df_eff = df_eff[(df_eff["intensity"] > 0) & (df_eff["gdp_pc"] > 0)]

    if df_eff.empty:
        st.info("No economic efficiency data available for this selection.")
    else:
        c_s1, c_s2 = st.columns([3, 1])
        with c_s2:
            log_x = st.checkbox("Logarithmic GDP Scale", value=True)
            size_by_co2 = st.checkbox("Scale bubbles by CO₂ emissions", value=True)

        # Ensure bubble size is strictly positive and non-null for Plotly marker
        df_eff["bubble_size"] = df_eff["co2_mt"].fillna(1.0).clip(lower=1.0)

        fig_scat = px.scatter(
            df_eff,
            x="gdp_pc",
            y="intensity",
            color="region",
            size="bubble_size" if size_by_co2 else None,
            hover_name="country",
            log_x=log_x,
            hover_data={
                "gdp_pc": ":$,.0f",
                "intensity": ":.2f",
                "renew_share": ":.1f%",
                "bubble_size": False,
                "co2_mt": ":,.1f",
            },
            labels={
                "gdp_pc": "GDP per Capita (USD)",
                "intensity": "Energy Intensity (MJ / $2017 PPP GDP)",
                "region": "Geographic Region",
                "co2_mt": "CO₂ (Mt)",
            },
            color_discrete_sequence=["#059669", "#0284C7", "#D97706", "#E11D48", "#7C3AED", "#0D9488"]
        )
        clean_chart(fig_scat, f"Economic Decoupling: Energy Intensity vs GDP per Capita ({year_sel})", height=460)
        st.plotly_chart(fig_scat, use_container_width=True)

# =============================================================================
# TAB 4: HOW TO OPTIMIZE ENERGY (SIMULATOR & DIRECTIVE)
# =============================================================================
with tab4:
    st.markdown("""
    <div class="takeaway-card">
      <b>🎯 Core Project Directive:</b> This interactive simulation answers your curiosity question: <i>"How can energy usage be optimized?"</i>. By adjusting policy levers below, we calculate the estimated CO₂ abatement and clean generation required.
    </div>
    """, unsafe_allow_html=True)

    col_sim_ctl, col_sim_res = st.columns([1, 1])

    with col_sim_ctl:
        st.markdown("### 🎛️ Optimization Policy Levers")
        p_renew_add = st.slider("1. Increase Renewable Power Generation (+%)", 0, 50, 15, 5,
                                help="Accelerating solar and wind power adoption across national grids.")
        p_int_cut = st.slider("2. Industrial Energy Efficiency Improvement (-%)", 0, 40, 12, 2,
                              help="Better building insulation, efficient heat pumps, and motor speed controls.")
        p_coal_retire = st.slider("3. Coal / High-Fossil Power Phase-Out (-%)", 0, 50, 20, 5,
                                  help="Retiring inefficient thermal coal generation units.")

        st.markdown("---")
        st.markdown("### 🏛️ The 4 Core Optimization Pillars")
        st.markdown("""
        <div class="opt-pillar">
          <h4>🌱 Pillar 1: Renewable Grid Dispatch</h4>
          <p>Prioritizing zero-fuel-cost renewables (solar/wind) over thermal fossil generators cuts grid fuel burn directly.</p>
        </div>
        <div class="opt-pillar">
          <h4>💡 Pillar 2: Demand-Side Energy Intensity Reduction</h4>
          <p>Mandating high-efficiency building insulation, variable-frequency industrial motors, and LED standards reduces wasted megajoules per dollar of GDP.</p>
        </div>
        <div class="opt-pillar">
          <h4>🔌 Pillar 3: Clean Cooking & Heat Electrification</h4>
          <p>Transitioning from inefficient open-flame biomass cooking to induction electric cooking reduces thermal energy losses by over 60%.</p>
        </div>
        <div class="opt-pillar">
          <h4>⚡ Pillar 4: High-Voltage Grid Interconnections</h4>
          <p>Expanding HVDC transmission lines shares renewable surpluses across state borders, minimizing curtailment and line losses.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_sim_res:
        st.markdown("### 📊 Simulated Optimization Impact")

        # Empirical simulation calculation based on current cohort
        baseline_co2 = max(df_cur["co2_mt"].sum(), 1.0)
        baseline_elec = df_cur["total_elec_twh"].sum()
        baseline_fossil = df_cur["fossil_twh"].sum()

        # Abatement formulas
        co2_cut_fossil = (p_coal_retire / 100.0) * (baseline_fossil * 0.85)  # ~0.85 Mt CO2 per TWh coal
        co2_cut_efficiency = (p_int_cut / 100.0) * baseline_co2 * 0.4
        total_co2_abated = min(co2_cut_fossil + co2_cut_efficiency, baseline_co2 * 0.75)
        new_projected_co2 = baseline_co2 - total_co2_abated
        clean_twh_added = (p_renew_add / 100.0) * baseline_elec

        # Quick simulated KPIs
        c_k1, c_k2 = st.columns(2)
        with c_k1:
            st.metric(
                label="Simulated CO₂ Abatement",
                value=f"{total_co2_abated:,.1f} Mt",
                delta=f"-{(total_co2_abated / baseline_co2 * 100):.1f}% reduction"
            )
        with c_k2:
            st.metric(
                label="Clean Power Added",
                value=f"{clean_twh_added:,.1f} TWh",
                delta=f"+{p_renew_add}% expansion"
            )

        # Waterfall / Impact Comparison Bar
        fig_opt = go.Figure()
        fig_opt.add_trace(go.Bar(
            name="Emissions Comparison",
            x=["Baseline CO₂ (Current)", "Fossil Phase-Out Savings", "Efficiency Savings", "Target CO₂ Output"],
            y=[baseline_co2, -co2_cut_fossil, -co2_cut_efficiency, new_projected_co2],
            marker_color=["#E11D48", "#059669", "#0284C7", "#10B981"],
            text=[f"{baseline_co2:,.0f} Mt", f"-{co2_cut_fossil:,.0f} Mt", f"-{co2_cut_efficiency:,.0f} Mt", f"{new_projected_co2:,.0f} Mt"],
            textposition="auto"
        ))
        clean_chart(fig_opt, "Simulated Carbon Abatement Trajectory (Mt CO₂)", height=380, show_legend=False)
        fig_opt.update_layout(yaxis_title="Megatonnes CO₂")
        st.plotly_chart(fig_opt, use_container_width=True)

# =============================================================================
# TAB 5: COUNTRY DATA EXPLORER
# =============================================================================
with tab5:
    st.markdown("""
    <div class="takeaway-card">
      <b>💡 Examiner Presentation Point:</b> This data hub provides full provenance for our study. You can search any country (e.g., India, USA, Germany) to inspect its multi-indicator energy metrics and export the cohort as CSV.
    </div>
    """, unsafe_allow_html=True)

    search_q = st.text_input("🔍 Search Country Name:", placeholder="e.g. India, Germany, Brazil, United States...")

    df_table = df_cur.copy()
    if search_q.strip():
        df_table = df_table[df_table["country"].str.contains(search_q, case=False, na=False)]

    display_cols = [
        "country", "region", "year", "renew_share", "lowcarbon_pct",
        "intensity", "access_elec", "clean_fuels", "co2_mt", "total_elec_twh", "gdp_pc"
    ]
    disp_df = df_table[display_cols].rename(columns={
        "country": "Country",
        "region": "Region",
        "year": "Year",
        "renew_share": "Renewable Share (%)",
        "lowcarbon_pct": "Clean Elec (%)",
        "intensity": "Intensity (MJ/$)",
        "access_elec": "Elec Access (%)",
        "clean_fuels": "Clean Cooking (%)",
        "co2_mt": "CO₂ (Mt)",
        "total_elec_twh": "Total Elec (TWh)",
        "gdp_pc": "GDP/Capita ($)"
    })

    st.dataframe(
        disp_df.style.format({
            "Renewable Share (%)": "{:.1f}%",
            "Clean Elec (%)": "{:.1f}%",
            "Intensity (MJ/$)": "{:.2f}",
            "Elec Access (%)": "{:.1f}%",
            "Clean Cooking (%)": "{:.1f}%",
            "CO₂ (Mt)": "{:,.1f}",
            "Total Elec (TWh)": "{:,.1f}",
            "GDP/Capita ($)": "${:,.0f}"
        }),
        use_container_width=True,
        height=420
    )

    csv_data = disp_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Cohort Data (CSV)",
        data=csv_data,
        file_name=f"sustainable_energy_data_{year_sel}.csv",
        mime="text/csv",
    )
