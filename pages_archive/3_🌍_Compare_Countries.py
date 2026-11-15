"""
🌍 Page 3 — Compare Countries
Side-by-side multi-metric country comparison with radar charts.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from data_loader import load_clean, COL, countries, filter_df, latest_year_country
from theme import CSS, COLORS, apply_layout, kpi, sec, insight, hero

st.set_page_config(page_title="🌍 Compare Countries", page_icon="🌍", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data(): return load_clean()
df_all = get_data()
all_c = countries(df_all)

PALETTE = [COLORS["teal"],COLORS["purple"],COLORS["amber"],COLORS["coral"],
           COLORS["sky"],COLORS["green"],COLORS["pink"],"#FB923C","#A78BFA","#6EE7B7"]

with st.sidebar:
    st.markdown("**🏳️ Select Countries to Compare**")
    sel = st.multiselect("", all_c,
        default=["India","China","United States","Germany","Brazil","Norway"],
        label_visibility="collapsed")
    yr = st.slider("Year", 2000, 2020, 2019)

sel = sel or ["India","China","United States","Germany","Brazil"]
df_yr = filter_df(df_all, sel, (yr, yr))

st.markdown(hero("🌍 Country Comparison", f"Multi-Metric Energy Benchmarking — {yr}"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Radar chart ───────────────────────────────────────────────────────────────
st.markdown(sec("📡 Radar — Multi-Metric Energy Profile"), unsafe_allow_html=True)

METRICS = {
    "Electricity Access": COL["elec_access"],
    "Renewable Share": COL["renew_share"],
    "Low-Carbon Elec": COL["lowcarbon"],
    "Clean Fuels": COL["clean_fuels"],
    "Energy Intensity\n(inverted)": COL["intensity"],
    "Renew Capacity/cap": COL["renew_cap"],
}

def normalize(series):
    mn, mx = series.min(), series.max()
    return (series - mn) / (mx - mn + 1e-9) * 100

norm_df = df_yr.copy()
for label, col in METRICS.items():
    if col in norm_df.columns:
        if "Intensity" in label:
            norm_df[col + "_n"] = 100 - normalize(norm_df[col].fillna(norm_df[col].median()))
        else:
            norm_df[col + "_n"] = normalize(norm_df[col].fillna(norm_df[col].median()))

cats = list(METRICS.keys())
n_cats = len(cats)

fig_rad = go.Figure()
for i, (_, row) in enumerate(norm_df.iterrows()):
    vals = []
    for label, col in METRICS.items():
        v = row.get(col + "_n", 50)
        vals.append(float(v) if not np.isnan(v) else 50)
    fig_rad.add_trace(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", name=row[COL["entity"]],
        line=dict(color=PALETTE[i % len(PALETTE)], width=2),
        fillcolor=PALETTE[i % len(PALETTE)].replace(")", ",0.12)").replace("rgb","rgba") if "rgb" in PALETTE[i % len(PALETTE)] else PALETTE[i % len(PALETTE)] + "1E",
        hovertemplate="<b>" + row[COL["entity"]] + "</b><br>%{theta}: %{r:.0f}/100<extra></extra>",
    ))
fig_rad.update_layout(
    polar=dict(
        bgcolor="#111827",
        radialaxis=dict(visible=True, range=[0,100], gridcolor=COLORS["grid"],
                        tickfont=dict(color=COLORS["sub"]), ticksuffix=""),
        angularaxis=dict(gridcolor=COLORS["grid"], linecolor=COLORS["grid"],
                         tickfont=dict(color=COLORS["text"])),
    ),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
    paper_bgcolor=COLORS["bg"], font=dict(color=COLORS["text"]),
    height=460, margin=dict(l=50,r=50,t=40,b=20),
    title=dict(text=f"🌐 Multi-Metric Radar — {yr} (all metrics normalised 0–100)", font=dict(size=13), x=0.5),
)
st.plotly_chart(fig_rad, use_container_width=True)

# ── Side-by-side bar metrics ───────────────────────────────────────────────────
st.markdown(sec("📊 Key Metrics — Side by Side"), unsafe_allow_html=True)
metrics_sel = st.multiselect("Metrics to compare", list(METRICS.keys()),
    default=["Electricity Access","Renewable Share","Low-Carbon Elec","Clean Fuels"],
    label_visibility="visible")

cols_chosen = [METRICS[m] for m in metrics_sel if m in METRICS]
n_m = len(cols_chosen)
if n_m > 0:
    rows_fig = (n_m + 1) // 2
    for row_i in range(rows_fig):
        pair = cols_chosen[row_i*2 : row_i*2+2]
        pair_names = metrics_sel[row_i*2 : row_i*2+2]
        sub_cols = st.columns(len(pair))
        for j, (col_key, m_name) in enumerate(zip(pair, pair_names)):
            with sub_cols[j]:
                fig_b = go.Figure()
                data_b = df_yr[[COL["entity"], col_key]].dropna().sort_values(col_key, ascending=False)
                fig_b.add_trace(go.Bar(
                    x=data_b[COL["entity"]],
                    y=data_b[col_key].round(2),
                    marker=dict(
                        color=data_b[col_key],
                        colorscale=[[0,"#F87171"],[0.5,"#F59E0B"],[1,"#00C9A7"]],
                        showscale=False,
                    ),
                    hovertemplate="<b>%{x}</b>: %{y:.2f}<extra></extra>",
                    text=data_b[col_key].round(1),
                    textposition="outside", textfont=dict(color=COLORS["text"], size=9),
                ))
                apply_layout(fig_b, m_name, 290)
                st.plotly_chart(fig_b, use_container_width=True)

# ── Time series comparison ────────────────────────────────────────────────────
st.markdown(sec("📈 Historical Comparison — Renewable Energy Share (%)"), unsafe_allow_html=True)
ts_df = filter_df(df_all, sel, (2000, 2020))
fig_ts = px.line(ts_df, x=COL["year"], y=COL["renew_share"], color=COL["entity"],
    color_discrete_sequence=PALETTE,
    markers=True,
    labels={COL["renew_share"]:"Renewable Share (%)", COL["year"]:"Year"},
)
fig_ts.update_traces(line_width=2.3, marker_size=5)
apply_layout(fig_ts, "Renewable Energy Share Over Time (%) — Selected Countries", 380)
st.plotly_chart(fig_ts, use_container_width=True)

# ── Summary table ─────────────────────────────────────────────────────────────
st.markdown(sec(f"📋 Full Data Table — {yr}"), unsafe_allow_html=True)
display_cols = [COL["entity"], COL["elec_access"], COL["renew_share"], COL["lowcarbon"],
                COL["energy_pc"], COL["intensity"], COL["co2"], COL["gdp_pc"], COL["clean_fuels"]]
display_df = df_yr[[c for c in display_cols if c in df_yr.columns]].copy()
rename = {
    COL["entity"]:      "Country",
    COL["elec_access"]: "Elec Access (%)",
    COL["renew_share"]: "Renewable Share (%)",
    COL["lowcarbon"]:   "Low-Carbon Elec (%)",
    COL["energy_pc"]:   "Energy/Capita (kWh)",
    COL["intensity"]:   "Intensity (MJ/$)",
    COL["co2"]:         "CO₂ (kt)",
    COL["gdp_pc"]:      "GDP/Capita (USD)",
    COL["clean_fuels"]: "Clean Fuels (%)",
}
display_df = display_df.rename(columns=rename).round(2).reset_index(drop=True)
st.dataframe(display_df, use_container_width=True, hide_index=True)

# Leader for each metric
leaders = {}
for m_name, col_key in METRICS.items():
    if col_key in df_yr.columns:
        sub = df_yr[[COL["entity"], col_key]].dropna()
        if not sub.empty:
            if "Intensity" in m_name:
                leaders[m_name] = sub.nsmallest(1, col_key)[COL["entity"]].values[0]
            else:
                leaders[m_name] = sub.nlargest(1, col_key)[COL["entity"]].values[0]

leaders_txt = " · ".join([f"**{v}** leads in {k.replace(chr(10),' ')}" for k,v in leaders.items()])
st.markdown(insight(
    f"**Country Comparison ({yr}):** {leaders_txt}. "
    f"These leaders demonstrate that strong renewable policy, grid investment, and economic development together "
    f"drive optimal sustainable energy outcomes."
), unsafe_allow_html=True)

