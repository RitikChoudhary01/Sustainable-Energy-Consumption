"""
📉 Page 2 — Energy Efficiency & Intensity
Energy intensity, consumption per capita, and efficiency trends.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from data_loader import load_clean, COL, countries, years, filter_df, world_agg, latest_year_country, region_map
from theme import CSS, COLORS, apply_layout, kpi, sec, insight, hero

st.set_page_config(page_title="📉 Efficiency", page_icon="📉", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data(): return load_clean()

df_all = get_data()
all_c = countries(df_all)

with st.sidebar:
    st.markdown("**🌍 Countries**")
    sel = st.multiselect("", all_c,
        default=["China","United States","Germany","India","Japan","United Kingdom","Brazil","South Korea"],
        label_visibility="collapsed")
    yr = st.slider("Year range", 2000, 2020, (2000, 2020))
    st.markdown("**📊 Compare metric**")
    cmp = st.selectbox("", ["Energy Intensity (MJ/$)", "Energy per Capita (kWh/person)"],
                        label_visibility="collapsed")

sel = sel or all_c
df = filter_df(df_all, sel, yr)
latest = latest_year_country(df)
world = world_agg(df_all)
ly = yr[1]
fy = yr[0]
lyr = df[df[COL["year"]] == ly]
fyr = df[df[COL["year"]] == fy]

st.markdown(hero("📉 Energy Efficiency & Intensity", "How efficiently is energy being used relative to economic output?"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# KPIs
avg_int_ly = lyr[COL["intensity"]].mean()
avg_int_fy = fyr[COL["intensity"]].mean()
avg_epc_ly = lyr[COL["energy_pc"]].mean()
avg_epc_fy = fyr[COL["energy_pc"]].mean()
best_int   = latest.nsmallest(1, COL["intensity"])[COL["entity"]].values[0]
worst_int  = latest.nlargest(1, COL["intensity"])[COL["entity"]].values[0]

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(kpi("📉", f"{avg_int_ly:.2f}", f"Avg Energy Intensity ({ly})",
    f"{'↓' if avg_int_ly<avg_int_fy else '↑'} {abs(avg_int_ly-avg_int_fy):.2f} vs {fy}", avg_int_ly<avg_int_fy), unsafe_allow_html=True)
with c2: st.markdown(kpi("🏭", f"{avg_epc_ly:,.0f}", f"Avg Energy/Capita ({ly}) kWh",
    f"{'↑' if avg_epc_ly>avg_epc_fy else '↓'} {abs(avg_epc_ly-avg_epc_fy):,.0f} vs {fy}", avg_epc_ly<avg_epc_fy), unsafe_allow_html=True)
with c3: st.markdown(kpi("🏆", best_int, "Most Efficient (Intensity)", f"lowest MJ/$ in {ly}", True), unsafe_allow_html=True)
with c4: st.markdown(kpi("⚠️", worst_int, "Least Efficient", f"highest MJ/$ in {ly}", False), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main line chart
st.markdown(sec(f"📈 Energy Intensity Trend — {cmp}"), unsafe_allow_html=True)
y_col = COL["intensity"] if "Intensity" in cmp else COL["energy_pc"]
y_lbl = "Energy Intensity (MJ/$ GDP)" if "Intensity" in cmp else "Energy per Capita (kWh/person)"

fig_line = px.line(df, x=COL["year"], y=y_col, color=COL["entity"],
    color_discrete_sequence=[COLORS["teal"],COLORS["purple"],COLORS["amber"],
                               COLORS["coral"],COLORS["sky"],COLORS["green"],
                               COLORS["pink"],"#FB923C"],
    markers=True, labels={y_col: y_lbl, COL["year"]: "Year"},
)
fig_line.update_traces(line_width=2.3, marker_size=5)
apply_layout(fig_line, f"📊 {y_lbl} by Country (2000–2020)", 390)
st.plotly_chart(fig_line, use_container_width=True)

# Bar race snapshot + intensity vs GDP
ca, cb = st.columns(2)
with ca:
    # Horizontal bar — latest year intensity ranking
    bar_d = lyr[[COL["entity"], COL["intensity"]]].dropna().sort_values(COL["intensity"])
    colors_bar = [COLORS["teal"] if v < bar_d[COL["intensity"]].median()
                  else COLORS["amber"] if v < bar_d[COL["intensity"]].quantile(.75)
                  else COLORS["coral"] for v in bar_d[COL["intensity"]]]
    fig_bar = go.Figure(go.Bar(
        x=bar_d[COL["intensity"]], y=bar_d[COL["entity"]],
        orientation="h", marker_color=colors_bar,
        hovertemplate="<b>%{y}</b>: %{x:.2f} MJ/$<extra></extra>",
        text=bar_d[COL["intensity"]].round(1),
        textposition="outside", textfont=dict(color=COLORS["text"], size=9),
    ))
    apply_layout(fig_bar, f"Energy Intensity Ranking — {ly} (lower = more efficient)", 420)
    st.plotly_chart(fig_bar, use_container_width=True)

with cb:
    # Scatter intensity vs GDP per capita
    sc = lyr[[COL["entity"],COL["intensity"],COL["gdp_pc"],COL["renew_share"]]].dropna()
    fig_sc = px.scatter(sc, x=COL["gdp_pc"], y=COL["intensity"],
        color=COL["renew_share"], size=COL["gdp_pc"],
        hover_name=COL["entity"],
        color_continuous_scale=[[0,"#F87171"],[0.5,"#F59E0B"],[1,"#00C9A7"]],
        log_x=True, size_max=35, opacity=0.78,
        trendline="ols",
        labels={COL["gdp_pc"]:"GDP per Capita (log)", COL["intensity"]:"Intensity (MJ/$)",
                COL["renew_share"]:"Renewable %"},
    )
    apply_layout(fig_sc, f"GDP per Capita vs Energy Intensity (colour = renewable %) — {ly}", 420)
    st.plotly_chart(fig_sc, use_container_width=True)

# Clean fuels + Energy per capita area
st.markdown(sec("🍳 Clean Fuels Access & Energy per Capita"), unsafe_allow_html=True)
cc, cd = st.columns(2)
with cc:
    cf_data = df[[COL["year"],COL["entity"],COL["clean_fuels"]]].dropna()
    fig_cf = px.line(cf_data, x=COL["year"], y=COL["clean_fuels"], color=COL["entity"],
        color_discrete_sequence=[COLORS["teal"],COLORS["purple"],COLORS["amber"],
                                   COLORS["coral"],COLORS["sky"],COLORS["green"],COLORS["pink"],"#FB923C"],
        markers=True,
        labels={COL["clean_fuels"]:"Clean Fuels Access (%)", COL["year"]:"Year"},
    )
    fig_cf.update_traces(line_width=2, marker_size=4)
    apply_layout(fig_cf, "🍳 Access to Clean Fuels for Cooking (%)", 360)
    st.plotly_chart(fig_cf, use_container_width=True)

with cd:
    # Energy per capita area chart
    epc_world = world[world[COL["year"]].between(yr[0], yr[1])]
    fig_epc = go.Figure()
    fig_epc.add_trace(go.Scatter(
        x=epc_world[COL["year"]], y=epc_world[COL["energy_pc"]].round(0),
        fill="tozeroy", mode="lines",
        line=dict(color=COLORS["purple"], width=2.5),
        fillcolor="rgba(132,94,247,0.15)",
        hovertemplate="Year %{x}: %{y:,.0f} kWh/person<extra></extra>",
        name="World avg",
    ))
    apply_layout(fig_epc, "🌍 World Average Primary Energy Consumption per Capita (kWh/person)", 360)
    st.plotly_chart(fig_epc, use_container_width=True)

# Heatmap: energy intensity by country × year
st.markdown(sec("🗺️ Energy Intensity Heatmap — Country × Year"), unsafe_allow_html=True)
hm_c = latest.nlargest(18, COL["energy_pc"])[COL["entity"]].tolist()
hm = df_all[df_all[COL["entity"]].isin(hm_c)].pivot_table(
    index=COL["entity"], columns=COL["year"], values=COL["intensity"])

fig_hm = go.Figure(go.Heatmap(
    z=hm.values, x=hm.columns.astype(str).tolist(), y=hm.index.tolist(),
    colorscale=[[0,"#00C9A7"],[0.4,"#F59E0B"],[0.8,"#F87171"],[1,"#7F1D1D"]],
    hovertemplate="<b>%{y}, %{x}</b><br>Intensity: %{z:.2f} MJ/$<extra></extra>",
    colorbar=dict(title=dict(text="MJ/$", font=dict(color=COLORS["sub"])),
                  tickfont=dict(color=COLORS["sub"]), thickness=12),
))
apply_layout(fig_hm, "Energy Intensity (MJ/$ GDP) — High-Energy Countries (green = efficient, red = inefficient)", 440)
st.plotly_chart(fig_hm, use_container_width=True)

eff_gain = abs((avg_int_fy - avg_int_ly) / (avg_int_fy + 1e-9)) * 100
st.markdown(insight(
    f"**Efficiency Insight:** Energy intensity across selected countries fell by **{eff_gain:.0f}%** from {fy} to {ly}. "
    f"This confirms that the global economy is producing more GDP per unit of energy consumed. "
    f"**{best_int}** is the most energy-efficient economy in {ly}. "
    f"Higher-income countries generally show lower intensity because their service-based economies use less energy per dollar of output. "
    f"Closing the efficiency gap in developing economies through technology transfer could prevent significant CO₂ growth."
), unsafe_allow_html=True)

