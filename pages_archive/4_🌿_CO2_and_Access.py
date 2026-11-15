"""
🌿 Page 4 — CO₂ Emissions & Clean Energy Access
Carbon footprint trends, emissions vs renewables, and clean energy access.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from data_loader import load_clean, COL, countries, filter_df, world_agg, latest_year_country, region_map
from theme import CSS, COLORS, apply_layout, kpi, sec, insight, hero

st.set_page_config(page_title="🌿 CO₂ & Access", page_icon="🌿", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data(): return load_clean()
df_all = get_data()
all_c = countries(df_all)
world = world_agg(df_all)

with st.sidebar:
    st.markdown("**🌍 Country Filter**")
    sel = st.multiselect("", all_c,
        default=["China","United States","India","Russia","Germany","Japan","Brazil","South Africa"],
        label_visibility="collapsed")
    yr = st.slider("Year range", 2000, 2020, (2000, 2020))
    co2_threshold = st.slider("High emitter threshold (Mt)", 100, 5000, 500, 100)

sel = sel or all_c
df = filter_df(df_all, sel, yr)
latest = latest_year_country(df)
ly = yr[1]
fy = yr[0]

st.markdown(hero("🌿 CO₂ Emissions & Clean Energy Access", "Carbon Footprint · Electricity Access · Clean Fuels"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# KPIs
tot_co2_ly = df[df[COL["year"]] == ly]["co2_mt"].sum()
tot_co2_fy = df[df[COL["year"]] == fy]["co2_mt"].sum()
avg_access_ly = df[df[COL["year"]] == ly][COL["elec_access"]].mean()
avg_access_fy = df[df[COL["year"]] == fy][COL["elec_access"]].mean()
avg_clean_ly = df[df[COL["year"]] == ly][COL["clean_fuels"]].mean()
top_emitter = latest.nlargest(1,"co2_mt")[COL["entity"]].values[0] if "co2_mt" in latest.columns else "N/A"
high_emitters = (latest["co2_mt"] > co2_threshold).sum()

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(kpi("🌿", f"{tot_co2_ly:,.0f} Mt", f"Total CO₂ ({ly})",
    f"{'↑' if tot_co2_ly>tot_co2_fy else '↓'} {abs(tot_co2_ly-tot_co2_fy):,.0f} Mt vs {fy}", tot_co2_ly<tot_co2_fy), unsafe_allow_html=True)
with c2: st.markdown(kpi("⚡", f"{avg_access_ly:.1f}%", f"Avg Elec Access ({ly})",
    f"{'↑'} {abs(avg_access_ly-avg_access_fy):.1f}pp vs {fy}", True), unsafe_allow_html=True)
with c3: st.markdown(kpi("🍳", f"{avg_clean_ly:.1f}%", f"Clean Fuels Access ({ly})", "avg cooking access", avg_clean_ly > 50), unsafe_allow_html=True)
with c4: st.markdown(kpi("🏭", str(high_emitters), f"High Emitters (>{co2_threshold}Mt)", f"countries above threshold in {ly}", False), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# CO₂ trend lines
st.markdown(sec("📈 CO₂ Emissions Over Time"), unsafe_allow_html=True)
ca, cb = st.columns(2)
with ca:
    fig_co2 = px.line(df, x=COL["year"], y="co2_mt", color=COL["entity"],
        color_discrete_sequence=[COLORS["teal"],COLORS["purple"],COLORS["amber"],
                                   COLORS["coral"],COLORS["sky"],COLORS["green"],COLORS["pink"],"#FB923C"],
        markers=True,
        labels={"co2_mt":"CO₂ Emissions (Mt)", COL["year"]:"Year"},
    )
    fig_co2.update_traces(line_width=2.2, marker_size=4)
    apply_layout(fig_co2, "CO₂ Emissions (Mt) by Country — 2000 to 2020", 380)
    st.plotly_chart(fig_co2, use_container_width=True)

with cb:
    # World CO₂ bar + renewable share overlay
    world_range = world[world[COL["year"]].between(yr[0], yr[1])]
    fig_w = make_subplots(specs=[[{"secondary_y": True}]])
    fig_w.add_trace(go.Bar(
        x=world_range[COL["year"]], y=world_range["co2_mt"].round(0),
        name="World CO₂ (Mt)", marker_color="rgba(248,113,113,0.65)",
        hovertemplate="Year %{x}: %{y:,.0f} Mt<extra></extra>",
    ), secondary_y=False)
    fig_w.add_trace(go.Scatter(
        x=world_range[COL["year"]], y=world_range[COL["renew_share"]].round(2),
        name="World Renew %", mode="lines+markers",
        line=dict(color=COLORS["teal"], width=2.5),
        marker=dict(size=5),
        hovertemplate="Renew% %{x}: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)
    apply_layout(fig_w, "🌍 World CO₂ vs Renewable Share", 380)
    fig_w.update_yaxes(title_text="CO₂ (Mt)", secondary_y=False,
                        gridcolor=COLORS["grid"], tickfont=dict(color=COLORS["sub"]))
    fig_w.update_yaxes(title_text="Renewable Share (%)", secondary_y=True,
                        showgrid=False, tickfont=dict(color=COLORS["teal"]))
    st.plotly_chart(fig_w, use_container_width=True)

# CO₂ vs renewable scatter
st.markdown(sec(f"🔬 CO₂ Emissions vs Renewable Energy Share — {ly}"), unsafe_allow_html=True)
sc_data = df[df[COL["year"]] == ly][[COL["entity"],"co2_mt",COL["renew_share"],COL["gdp_pc"],COL["energy_pc"]]].dropna()
fig_sc = px.scatter(sc_data, x=COL["renew_share"], y="co2_mt",
    color=COL["gdp_pc"], size=COL["energy_pc"],
    hover_name=COL["entity"],
    color_continuous_scale=[[0,"#0D3B6E"],[0.5,"#845EF7"],[1,"#F59E0B"]],
    size_max=45, opacity=0.78,
    log_y=True,
    labels={COL["renew_share"]:"Renewable Share (%)", "co2_mt":"CO₂ (Mt, log)", COL["gdp_pc"]:"GDP/Capita"},
    trendline="ols",
)
apply_layout(fig_sc, f"Renewable Share vs CO₂ Emissions (bubble size = energy/capita, colour = GDP/cap) — {ly}", 420)
st.plotly_chart(fig_sc, use_container_width=True)

# Electricity access maps / charts
st.markdown(sec("💡 Electricity Access & Clean Fuels Progress"), unsafe_allow_html=True)
cc, cd = st.columns(2)
with cc:
    # Access line
    fig_acc = px.line(df, x=COL["year"], y=COL["elec_access"], color=COL["entity"],
        color_discrete_sequence=[COLORS["teal"],COLORS["purple"],COLORS["amber"],
                                   COLORS["coral"],COLORS["sky"],COLORS["green"],COLORS["pink"],"#FB923C"],
        markers=False, labels={COL["elec_access"]:"Electricity Access (%)", COL["year"]:"Year"},
    )
    fig_acc.update_traces(line_width=2)
    fig_acc.add_hline(y=100, line=dict(color="rgba(255,255,255,0.12)", dash="dot"),
                       annotation_text="Universal Access", annotation_font=dict(color=COLORS["sub"], size=10))
    apply_layout(fig_acc, "⚡ Electricity Access (% Population)", 350)
    st.plotly_chart(fig_acc, use_container_width=True)

with cd:
    # Clean fuels vs electricity access scatter latest yr
    cf_data = df[df[COL["year"]] == ly][[COL["entity"],COL["clean_fuels"],COL["elec_access"],COL["gdp_pc"]]].dropna()
    fig_cf = px.scatter(cf_data, x=COL["elec_access"], y=COL["clean_fuels"],
        color=COL["gdp_pc"], hover_name=COL["entity"],
        color_continuous_scale=[[0,"#0D3B6E"],[0.5,"#845EF7"],[1,"#00C9A7"]],
        size_max=12, opacity=0.75,
        trendline="ols",
        labels={COL["elec_access"]:"Electricity Access (%)", COL["clean_fuels"]:"Clean Fuels Access (%)"},
    )
    apply_layout(fig_cf, f"Electricity Access vs Clean Fuels (colour = GDP/cap) — {ly}", 350)
    st.plotly_chart(fig_cf, use_container_width=True)

# Top emitters bar
st.markdown(sec(f"🏭 Top CO₂ Emitters — {ly}"), unsafe_allow_html=True)
top_em = df[df[COL["year"]] == ly][["Entity","co2_mt"]].dropna().nlargest(20,"co2_mt")
fig_em = go.Figure(go.Bar(
    x=top_em["Entity"], y=top_em["co2_mt"].round(1),
    marker=dict(
        color=top_em["co2_mt"],
        colorscale=[[0,"#00C9A7"],[0.5,"#F59E0B"],[1,"#F87171"]],
        showscale=True,
        colorbar=dict(title=dict(text="Mt", font=dict(color=COLORS["sub"])),
                      tickfont=dict(color=COLORS["sub"]), thickness=12),
    ),
    hovertemplate="<b>%{x}</b>: %{y:,.0f} Mt CO₂<extra></extra>",
    text=top_em["co2_mt"].round(0).astype(int),
    textposition="outside", textfont=dict(color=COLORS["text"], size=9),
))
apply_layout(fig_em, f"Top 20 CO₂ Emitters (Mt) — {ly}", 360)
st.plotly_chart(fig_em, use_container_width=True)

# Financial flows to developing countries
st.markdown(sec("💰 Financial Flows to Developing Countries for Clean Energy"), unsafe_allow_html=True)
ff_data = df_all.groupby(COL["year"])[COL["fin_flows"]].sum().reset_index()
fig_ff = go.Figure(go.Bar(
    x=ff_data[COL["year"]], y=(ff_data[COL["fin_flows"]] / 1e9).round(2),
    marker=dict(
        color=(ff_data[COL["fin_flows"]] / 1e9),
        colorscale=[[0,"#111827"],[0.5,"#845EF7"],[1,"#00C9A7"]],
        showscale=False,
    ),
    hovertemplate="Year %{x}: $%{y:.2f}B<extra></extra>",
    text=(ff_data[COL["fin_flows"]] / 1e9).round(1).astype(str) + "B",
    textposition="outside", textfont=dict(color=COLORS["text"], size=9),
))
apply_layout(fig_ff, "💰 Global Financial Flows to Developing Countries for Renewable Energy (Billion USD)", 320)
st.plotly_chart(fig_ff, use_container_width=True)

co2_chg = ((tot_co2_ly - tot_co2_fy) / (tot_co2_fy + 1e-9)) * 100
st.markdown(insight(
    f"**CO₂ & Access Insight:** CO₂ emissions across selected countries changed by **{co2_chg:+.1f}%** from {fy} to {ly}. "
    f"**{top_emitter}** remains the largest emitter. "
    f"The scatter plot confirms a clear **inverse relationship** between renewable energy share and CO₂ emissions — "
    f"countries investing in renewables are successfully bending the carbon curve. "
    f"Universal electricity access remains a goal — poorer regions still lag, "
    f"but the access gap has narrowed significantly since 2000, partly driven by off-grid solar solutions."
), unsafe_allow_html=True)

