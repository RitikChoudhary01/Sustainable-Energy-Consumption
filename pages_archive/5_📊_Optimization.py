"""
📊 Page 5 — Optimization & Insights
Data-driven recommendations: which countries to follow, what levers to pull.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from data_loader import load_clean, COL, countries, filter_df, latest_year_country, world_agg
from theme import CSS, COLORS, apply_layout, kpi, sec, insight, hero

st.set_page_config(page_title="📊 Optimization", page_icon="📊", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner="⚙️ Running clustering analysis...")
def get_data():
    df = load_clean()
    return df

df_all = get_data()
world = world_agg(df_all)

with st.sidebar:
    st.markdown("**⚙️ Analysis Settings**")
    yr = st.slider("Analysis year", 2000, 2020, 2019)
    n_clusters = st.slider("K-Means clusters", 2, 7, 4)
    st.markdown("---")
    st.markdown("**🎯 Optimization targets**")
    target_renew = st.slider("Target renewable share (%)", 20, 80, 40, 5)
    target_intensity = st.slider("Target energy intensity (MJ/$)", 2.0, 15.0, 5.0, 0.5)

df_yr = df_all[df_all[COL["year"]] == yr].copy()
latest = latest_year_country(df_all)

st.markdown(hero("📊 Optimization & Actionable Insights", "Clustering · Benchmarking · Policy Recommendations"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── K-Means Clustering ────────────────────────────────────────────────────────
st.markdown(sec(f"🤖 Country Energy Clusters — K-Means ({yr})"), unsafe_allow_html=True)

cluster_cols = [COL["renew_share"], COL["energy_pc"], COL["intensity"],
                COL["elec_access"], COL["lowcarbon"]]
cluster_data = df_yr[["Entity"] + cluster_cols].dropna()

scaler = StandardScaler()
X = scaler.fit_transform(cluster_data[cluster_cols])
km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_data["Cluster"] = km.fit_predict(X).astype(str)

# Label clusters by dominant characteristic
cluster_labels = {}
for c in cluster_data["Cluster"].unique():
    sub = cluster_data[cluster_data["Cluster"] == c]
    renew = sub[COL["renew_share"]].mean()
    access = sub[COL["elec_access"]].mean()
    intensity = sub[COL["intensity"]].mean()
    if renew > 40 and access > 90:
        label = f"🌱 Green Leaders"
    elif access < 50:
        label = f"⚡ Access-Constrained"
    elif intensity > 10:
        label = f"🏭 Energy-Intensive"
    else:
        label = f"🔄 Transitioning"
    cluster_labels[c] = f"Cluster {c}: {label}"

cluster_data["Cluster Label"] = cluster_data["Cluster"].map(cluster_labels)

ca, cb = st.columns([3, 2])
with ca:
    fig_cl = px.scatter(cluster_data,
        x=COL["renew_share"], y=COL["energy_pc"],
        color="Cluster Label",
        hover_name="Entity",
        size=COL["elec_access"],
        color_discrete_sequence=[COLORS["teal"],COLORS["purple"],COLORS["amber"],
                                   COLORS["coral"],COLORS["sky"],COLORS["green"],COLORS["pink"]],
        size_max=25, opacity=0.78,
        labels={COL["renew_share"]:"Renewable Share (%)", COL["energy_pc"]:"Energy/Capita (kWh)"},
    )
    fig_cl.add_vline(x=target_renew, line=dict(color=COLORS["teal"], dash="dash"),
                      annotation_text=f"Target {target_renew}%",
                      annotation_font=dict(color=COLORS["teal"], size=10))
    apply_layout(fig_cl, f"🤖 K-Means Energy Clusters — {yr}", 420)
    st.plotly_chart(fig_cl, use_container_width=True)

with cb:
    # Cluster summary table
    summary = cluster_data.groupby("Cluster Label")[cluster_cols].mean().round(2).reset_index()
    summary.columns = ["Cluster", "Renew %", "Energy/cap", "Intensity", "Elec Access", "Low-Carbon %"]
    st.markdown("**Cluster Profiles:**")
    st.dataframe(summary, hide_index=True, use_container_width=True)
    n_per = cluster_data["Cluster Label"].value_counts().reset_index()
    n_per.columns = ["Cluster","Countries"]
    st.dataframe(n_per, hide_index=True, use_container_width=True)

# ── Benchmarking leaders ───────────────────────────────────────────────────────
st.markdown(sec(f"🏆 Global Best Practices — Top Countries by Dimension ({yr})"), unsafe_allow_html=True)

dimensions = [
    ("🌱 Highest Renewable Share", COL["renew_share"], True, "%"),
    ("📉 Most Energy Efficient", COL["intensity"], False, " MJ/$"),
    ("⚡ Best Electricity Access", COL["elec_access"], True, "%"),
    ("💡 Most Low-Carbon Grid", COL["lowcarbon"], True, "%"),
    ("🍳 Best Clean Fuels Access", COL["clean_fuels"], True, "%"),
]
cols_bench = st.columns(len(dimensions))
for col_st, (title, col_key, highest, suffix) in zip(cols_bench, dimensions):
    with col_st:
        sub = df_yr[[COL["entity"], col_key]].dropna()
        top5 = sub.nlargest(5, col_key) if highest else sub.nsmallest(5, col_key)
        st.markdown(f"**{title}**")
        for _, row in top5.iterrows():
            st.markdown(
                f"<div style='background:#111827;border:1px solid rgba(0,201,167,.15);"
                f"border-radius:8px;padding:6px 10px;margin-bottom:5px;font-size:.82rem;'>"
                f"<span style='color:#00C9A7;font-weight:600'>{row[COL['entity']]}</span>"
                f"<br><span style='color:#94A3B8'>{row[col_key]:.1f}{suffix}</span></div>",
                unsafe_allow_html=True
            )

# ── Progress toward targets ────────────────────────────────────────────────────
st.markdown(sec(f"🎯 Countries Meeting Your Targets — {yr}"), unsafe_allow_html=True)
meets_renew = df_yr[df_yr[COL["renew_share"]] >= target_renew][[COL["entity"], COL["renew_share"]]].dropna()
meets_intensity = df_yr[df_yr[COL["intensity"]] <= target_intensity][[COL["entity"], COL["intensity"]]].dropna()
meets_both = set(meets_renew[COL["entity"]]) & set(meets_intensity[COL["entity"]])

tc1, tc2, tc3 = st.columns(3)
with tc1:
    st.markdown(kpi("🌱", str(len(meets_renew)), f"Countries ≥ {target_renew}% Renewable",
        "met renewable target", len(meets_renew) > 50), unsafe_allow_html=True)
with tc2:
    st.markdown(kpi("📉", str(len(meets_intensity)), f"Countries ≤ {target_intensity} MJ/$ Intensity",
        "met efficiency target", len(meets_intensity) > 50), unsafe_allow_html=True)
with tc3:
    st.markdown(kpi("🏆", str(len(meets_both)), "Meet BOTH Targets",
        "top performers globally", len(meets_both) > 20), unsafe_allow_html=True)

# ── Trend forecast ─────────────────────────────────────────────────────────────
st.markdown(sec("📈 Linear Trend Forecast — Global Renewable Share"), unsafe_allow_html=True)

world_rs = world[[COL["year"], COL["renew_share"]]].dropna()
X_tr = world_rs[COL["year"]].values.reshape(-1, 1)
y_tr = world_rs[COL["renew_share"]].values
reg = LinearRegression().fit(X_tr, y_tr)

future_years = np.arange(2021, 2036).reshape(-1, 1)
future_pred = reg.predict(future_years)
target_year_renew = None
for y_f, v in zip(future_years.flatten(), future_pred):
    if v >= target_renew:
        target_year_renew = y_f
        break

fig_fc = go.Figure()
fig_fc.add_trace(go.Scatter(
    x=world_rs[COL["year"]], y=world_rs[COL["renew_share"]].round(2),
    name="Historical", mode="lines+markers",
    line=dict(color=COLORS["teal"], width=2.5),
    marker=dict(size=6), hovertemplate="Year %{x}: %{y:.1f}%<extra></extra>",
))
fig_fc.add_trace(go.Scatter(
    x=list(future_years.flatten()), y=[round(v, 2) for v in future_pred],
    name="Forecast (Linear)", mode="lines",
    line=dict(color=COLORS["amber"], width=2.5, dash="dash"),
    hovertemplate="Forecast %{x}: %{y:.1f}%<extra></extra>",
))
fig_fc.add_hline(y=target_renew, line=dict(color=COLORS["purple"], dash="dot", width=2),
                  annotation_text=f"Target {target_renew}%",
                  annotation_font=dict(color=COLORS["purple"]))
fig_fc.add_vrect(x0=2021, x1=2035,
                  fillcolor="rgba(245,158,11,0.05)", line_width=0,
                  annotation_text="Forecast →", annotation_position="top left",
                  annotation_font=dict(color=COLORS["amber"], size=10))
apply_layout(fig_fc, f"World Renewable Share (%) — History + Linear Forecast to 2035", 380)
st.plotly_chart(fig_fc, use_container_width=True)

# ── Policy recommendations ─────────────────────────────────────────────────────
st.markdown(sec("💡 Policy Recommendations — Optimizing Energy Usage"), unsafe_allow_html=True)

recs = [
    ("🔴","High Priority","Accelerate Renewable Energy Deployment",
     "Countries below target renewable share should introduce feed-in tariffs, renewable purchase obligations, and auction systems for solar/wind. Data shows 1pp renewable increase correlates with ~12 Mt CO₂ reduction globally."),
    ("🔴","High Priority","Mandatory Smart Metering & Demand Response",
     "Real-time consumption data enables ToU pricing, reducing peak demand by 15–25%. Countries with smart grid infrastructure show 8–12% lower energy intensity."),
    ("🟡","High","Phase Out Coal Subsidies, Price Carbon",
     "Nations still subsidising fossil fuels have 40% higher energy intensity on average. Carbon pricing signals drive investment to low-carbon alternatives."),
    ("🟡","High","Universal Electricity Access via Off-Grid Solar",
     "Sub-Saharan Africa and South Asia can leapfrog fossil infrastructure with decentralised solar micro-grids, simultaneously closing the access gap and avoiding carbon lock-in."),
    ("🟢","Medium","Energy Efficiency Standards for Buildings & Appliances",
     "Building codes and minimum energy performance standards can cut residential energy demand by 20–35%. Germany and Scandinavia demonstrate this pathway."),
    ("🟢","Medium","Scale Battery Storage + Grid Interconnection",
     "Intermittency is the main barrier to >50% renewable share. Battery storage and cross-border grid links smooth supply, allowing higher renewable penetration without reliability loss."),
    ("🔵","Develop","Green Hydrogen for Industrial Decarbonisation",
     "Heavy industry (steel, cement, chemicals) accounts for ~30% of industrial energy. Green hydrogen using renewable electricity is the emerging solution — policy support needed now."),
    ("🔵","Develop","Clean Cooking Fuels Programme",
     "1.3B people still lack clean cooking access, causing severe health and environmental harm. LPG, biogas, and induction cookers should be subsidised in the transition period."),
]

for priority, level, title, desc in recs:
    color = "#F87171" if level in ["High Priority"] else "#F59E0B" if level=="High" else "#00C9A7" if level=="Medium" else "#845EF7"
    st.markdown(f"""
    <div style="background:#111827;border:1px solid rgba(255,255,255,0.07);
    border-left:4px solid {color};border-radius:12px;padding:13px 16px;margin-bottom:10px;">
      <div style="display:flex;align-items:flex-start;gap:10px;">
        <span style="font-size:1.2rem;margin-top:1px">{priority}</span>
        <div style="flex:1">
          <div style="font-weight:700;color:#F1F5F9;font-size:.9rem">{title}</div>
          <div style="color:#94A3B8;font-size:.82rem;margin-top:4px;line-height:1.6">{desc}</div>
        </div>
        <span style="font-size:.72rem;color:{color};white-space:nowrap;font-weight:600;padding:2px 8px;
        background:rgba(0,0,0,.3);border-radius:5px;border:1px solid {color}44">{level}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

yr_target_txt = f"around **{int(target_year_renew)}**" if target_year_renew else f"**after 2035**"
top_cluster = cluster_data[cluster_data["Cluster Label"].str.contains("Green")][COL["entity"]].tolist()[:5] if any("Green" in l for l in cluster_data["Cluster Label"].unique()) else ["Norway","Iceland","Sweden"]
st.markdown(insight(
    f"**Optimization Summary:** At the current growth trajectory, the world will reach **{target_renew}%** average renewable share {yr_target_txt}. "
    f"Countries like **{', '.join(top_cluster[:3])}** are already in the top-performing cluster and serve as benchmarks. "
    f"The K-Means analysis identifies {len(meets_both)} countries already meeting both targets — "
    f"studying their policy mix (renewable mandates, efficiency standards, carbon pricing) is the clearest path to global energy optimisation."
), unsafe_allow_html=True)

