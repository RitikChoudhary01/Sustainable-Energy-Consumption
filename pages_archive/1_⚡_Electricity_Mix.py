"""
⚡ Page 1 — Electricity Mix Analysis
Fossil vs Nuclear vs Renewable breakdown by country and year.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from data_loader import load_clean, COL, countries, years, filter_df, world_agg, latest_year_country
from theme import CSS, COLORS, apply_layout, kpi, sec, insight, hero

st.set_page_config(page_title="⚡ Electricity Mix", page_icon="⚡", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data(): return load_clean()

df_all = get_data()
all_countries = countries(df_all)

with st.sidebar:
    st.markdown("**🌍 Country Selection**")
    sel = st.multiselect("Countries", all_countries,
        default=["China","United States","Germany","India","Brazil","France","Japan","Australia"],
        label_visibility="collapsed")
    yr_range = st.slider("Year range", 2000, 2020, (2000, 2020))

sel = sel or all_countries
df = filter_df(df_all, sel, yr_range)
latest = latest_year_country(df)
ly = yr_range[1]

st.markdown(hero("⚡ Electricity Mix Analysis", "Fossil vs Nuclear vs Renewable — Country & Global Breakdown"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# KPIs
tot_r = latest[COL["renew_twh"]].sum()
tot_f = latest[COL["fossil_twh"]].sum()
tot_n = latest[COL["nuclear_twh"]].sum()
total = tot_r + tot_f + tot_n
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(kpi("🌱", f"{tot_r:,.0f} TWh", "Renewable Gen", f"{tot_r/total*100:.1f}% of total", True), unsafe_allow_html=True)
with c2: st.markdown(kpi("🏭", f"{tot_f:,.0f} TWh", "Fossil Gen", f"{tot_f/total*100:.1f}% of total", False), unsafe_allow_html=True)
with c3: st.markdown(kpi("☢️", f"{tot_n:,.0f} TWh", "Nuclear Gen", f"{tot_n/total*100:.1f}% of total", True), unsafe_allow_html=True)
with c4: st.markdown(kpi("💡", f"{latest[COL['lowcarbon']].mean():.1f}%", "Avg Low-Carbon", "nuclear + renewables", True), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Stacked bar by country
st.markdown(sec(f"🏭 Electricity Generation Mix by Country ({ly})"), unsafe_allow_html=True)
bar_data = df[df[COL["year"]] == ly].sort_values(COL["renew_twh"], ascending=False).head(25)

fig_stack = go.Figure()
for src, col_key, color in [
    ("Renewables", COL["renew_twh"], COLORS["teal"]),
    ("Nuclear", COL["nuclear_twh"], COLORS["purple"]),
    ("Fossil Fuels", COL["fossil_twh"], COLORS["coral"]),
]:
    fig_stack.add_trace(go.Bar(
        y=bar_data[COL["entity"]], x=bar_data[col_key].fillna(0).round(1),
        name=src, orientation="h", marker_color=color,
        hovertemplate=f"<b>%{{y}}</b> — {src}: %{{x:,.0f}} TWh<extra></extra>",
    ))
fig_stack.update_layout(barmode="stack")
apply_layout(fig_stack, f"Stacked Electricity Generation by Source (TWh) — {ly}", 500)
st.plotly_chart(fig_stack, use_container_width=True)

# Grouped line — renewable TWh over time top 8 countries
st.markdown(sec("📈 Renewable Electricity Growth Over Time"), unsafe_allow_html=True)
top8 = latest.nlargest(8, COL["renew_twh"])[COL["entity"]].tolist()
top8_data = df_all[df_all[COL["entity"]].isin(top8)]

ca, cb = st.columns(2)
with ca:
    fig_line = px.line(top8_data, x=COL["year"], y=COL["renew_twh"], color=COL["entity"],
        color_discrete_sequence=[COLORS["teal"],COLORS["purple"],COLORS["amber"],
                                   COLORS["coral"],COLORS["sky"],COLORS["green"],COLORS["pink"],"#FB923C"],
        markers=True, labels={COL["renew_twh"]:"Renewables (TWh)", COL["year"]:"Year"})
    fig_line.update_traces(line_width=2.2, marker_size=5)
    apply_layout(fig_line, "Top Countries — Renewable Generation (TWh)", 370)
    st.plotly_chart(fig_line, use_container_width=True)

with cb:
    # Donut — latest year global mix
    world_ly = world_agg(df_all[df_all[COL["year"]] == ly])
    r = float(world_ly[COL["renew_twh"]].iloc[0])
    n = float(world_ly[COL["nuclear_twh"]].iloc[0])
    f = float(world_ly[COL["fossil_twh"]].iloc[0])
    fig_donut = go.Figure(go.Pie(
        labels=["Renewables","Nuclear","Fossil Fuels"],
        values=[r, n, f], hole=0.62,
        marker=dict(colors=[COLORS["teal"],COLORS["purple"],COLORS["coral"]],
                    line=dict(color="#0A0E1A", width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color=COLORS["text"]),
        hovertemplate="<b>%{label}</b>: %{value:,.0f} TWh (%{percent})<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>{r+n+f:,.0f}</b><br><span style='font-size:9px'>TWh Total</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(size=16, color=COLORS["text"]),
    )
    apply_layout(fig_donut, f"🌍 Global Electricity Mix — {ly}", 370)
    st.plotly_chart(fig_donut, use_container_width=True)

# Low-carbon % heatmap
st.markdown(sec("🗓️ Low-Carbon Electricity — Country × Year Heatmap"), unsafe_allow_html=True)
hm_countries = latest.nlargest(20, COL["lowcarbon"])[COL["entity"]].tolist()
hm_data = df_all[df_all[COL["entity"]].isin(hm_countries)]
pivot = hm_data.pivot_table(index=COL["entity"], columns=COL["year"], values=COL["lowcarbon"])

fig_heat = go.Figure(go.Heatmap(
    z=pivot.values,
    x=pivot.columns.astype(str).tolist(),
    y=pivot.index.tolist(),
    colorscale=[[0,"#0A0E1A"],[0.3,"#0D3B6E"],[0.6,"#00C9A7"],[1,"#F59E0B"]],
    hovertemplate="<b>%{y}, %{x}</b><br>Low-Carbon: %{z:.1f}%<extra></extra>",
    colorbar=dict(title=dict(text="%", font=dict(color=COLORS["sub"])),
                  tickfont=dict(color=COLORS["sub"]), thickness=12),
))
apply_layout(fig_heat, "Low-Carbon Electricity (%) — Top 20 Countries by Low-Carbon Share", 420)
st.plotly_chart(fig_heat, use_container_width=True)

# Scatter — renewable capacity vs renewable share
st.markdown(sec("🔬 Renewable Capacity vs Renewable Share"), unsafe_allow_html=True)
sc_data = df[df[COL["year"]] == ly][[COL["entity"], COL["renew_cap"], COL["renew_share"], COL["gdp_pc"]]].dropna()
fig_sc = px.scatter(sc_data, x=COL["renew_cap"], y=COL["renew_share"],
    size=COL["gdp_pc"], hover_name=COL["entity"],
    color=COL["renew_share"],
    color_continuous_scale=[[0,"#F87171"],[0.5,"#F59E0B"],[1,"#00C9A7"]],
    size_max=40, opacity=0.75,
    labels={COL["renew_cap"]:"Renewable Capacity per Capita (W)",
            COL["renew_share"]:"Renewable Share (%)",
            COL["gdp_pc"]:"GDP per Capita"},
    trendline="ols",
)
apply_layout(fig_sc, f"Renewable Capacity per Capita vs Renewable Share — {ly}", 400)
st.plotly_chart(fig_sc, use_container_width=True)

best = bar_data.nlargest(1, COL["renew_twh"])[COL["entity"]].values[0]
worst_access = latest.nsmallest(1, COL["lowcarbon"])[COL["entity"]].values[0]
st.markdown(insight(
    f"**Electricity Mix:** **{best}** generates the most renewable electricity among selected countries in {ly}. "
    f"Countries with higher renewable generating capacity per capita tend to have higher renewable shares in their mix. "
    f"Nuclear power remains a vital low-carbon source — France and several European countries rely on it for >50% of their electricity. "
    f"The global trend shows fossil fuels still dominate, but the renewable share is growing rapidly — "
    f"particularly solar and wind, which have seen exponential capacity additions post-2010."
), unsafe_allow_html=True)

