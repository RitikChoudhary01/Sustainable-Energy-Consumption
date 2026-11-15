"""
Shared utilities: CSS theme + reusable HTML card helpers.
"""

# ─────────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Page & sidebar ── */
.stApp { background: linear-gradient(145deg,#0A0E1A 0%,#0D1526 60%,#0A1628 100%); }
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#0A0E1A 0%,#111827 100%);
  border-right: 1px solid rgba(0,201,167,0.12);
}

/* ── KPI cards ── */
.kpi-card {
  background: linear-gradient(135deg,rgba(17,24,39,0.95),rgba(15,20,35,0.95));
  border: 1px solid rgba(0,201,167,0.18);
  border-radius: 18px;
  padding: 22px 20px 18px;
  text-align: center;
  transition: transform .25s, box-shadow .25s, border-color .25s;
  box-shadow: 0 4px 28px rgba(0,0,0,.35);
  position: relative;
  overflow: hidden;
}
.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg,#00C9A7,#845EF7);
  border-radius: 18px 18px 0 0;
}
.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 36px rgba(0,201,167,.15);
  border-color: rgba(0,201,167,.4);
}
.kpi-icon  { font-size: 1.9rem; margin-bottom: 6px; }
.kpi-val   { font-size: 1.9rem; font-weight: 800; color: #00C9A7; line-height: 1.1; }
.kpi-label { font-size: .72rem; color: #94A3B8; text-transform: uppercase;
             letter-spacing: .09em; margin-top: 5px; }
.kpi-delta { font-size: .78rem; margin-top: 5px; }
.up   { color: #34D399; }
.down { color: #F87171; }

/* ── Section headers ── */
.sec-hdr {
  font-size: 1rem; font-weight: 700; color: #F1F5F9;
  padding: 8px 0 6px;
  border-bottom: 2px solid rgba(0,201,167,.25);
  margin: 6px 0 14px;
  letter-spacing: .02em;
}

/* ── Insight box ── */
.insight {
  background: linear-gradient(135deg,rgba(0,201,167,.07),rgba(132,94,247,.07));
  border: 1px solid rgba(0,201,167,.22);
  border-left: 4px solid #00C9A7;
  border-radius: 10px;
  padding: 14px 18px;
  font-size: .87rem;
  color: #E2E8F0;
  line-height: 1.65;
  margin: 10px 0;
}

/* ── Hero title ── */
.hero { text-align:center; padding: 10px 0 4px; }
.hero h1 {
  background: linear-gradient(90deg,#00C9A7 0%,#845EF7 50%,#F59E0B 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  font-size: 2.5rem; font-weight: 900; letter-spacing: -.03em; margin: 0;
}
.hero p { color: #64748B; font-size: .92rem; margin-top: 5px; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(17,24,39,.7); border-radius: 12px; padding: 4px; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 9px; color: #94A3B8 !important;
  font-weight: 500; font-size: .84rem; padding: 7px 18px;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg,rgba(0,201,167,.18),rgba(132,94,247,.18)) !important;
  color: #00C9A7 !important;
  border: 1px solid rgba(0,201,167,.28) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg,#00C9A7,#845EF7);
  color:#fff; border:none; border-radius:9px; font-weight:600;
  transition: all .2s;
}
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 4px 16px rgba(0,201,167,.3); }

/* ── Dataframe ── */
.stDataFrame { background:#111827; border-radius:12px; overflow:hidden; }

/* ── Progress ── */
.stProgress > div > div { background:linear-gradient(90deg,#00C9A7,#845EF7); border-radius:4px; }

/* ── Selectbox / slider ── */
.stSelectbox label, .stMultiSelect label, .stSlider label { color:#94A3B8 !important; font-size:.82rem !important; }
</style>
"""

COLORS = {
    "teal":    "#00C9A7",
    "purple":  "#845EF7",
    "amber":   "#F59E0B",
    "coral":   "#F87171",
    "sky":     "#38BDF8",
    "green":   "#34D399",
    "pink":    "#F472B6",
    "bg":      "#0A0E1A",
    "card":    "#111827",
    "grid":    "rgba(255,255,255,0.055)",
    "text":    "#F1F5F9",
    "sub":     "#94A3B8",
}

PLOT_LAYOUT = dict(
    paper_bgcolor="#0A0E1A",
    plot_bgcolor="#111827",
    font=dict(family="Inter, sans-serif", color="#F1F5F9", size=12),
    margin=dict(l=12, r=12, t=38, b=12),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11), bordercolor="rgba(255,255,255,.08)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.055)", zerolinecolor="rgba(255,255,255,0.055)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.055)", zerolinecolor="rgba(255,255,255,0.055)"),
    hoverlabel=dict(bgcolor="#111827", font_size=12, font_family="Inter"),
)


def apply_layout(fig, title="", height=380):
    fig.update_layout(**PLOT_LAYOUT,
        height=height,
        title=dict(text=title, font=dict(size=13, color="#F1F5F9"), x=0.01, xanchor="left")
    )
    return fig


def kpi(icon, val, label, delta="", good=True):
    dc = "up" if good else "down"
    dh = f'<div class="kpi-delta {dc}">{delta}</div>' if delta else ""
    return f"""<div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-val">{val}</div>
      <div class="kpi-label">{label}</div>{dh}
    </div>"""


def sec(title): return f'<div class="sec-hdr">{title}</div>'
def insight(txt): return f'<div class="insight">💡 {txt}</div>'
def hero(h1, sub): return f'<div class="hero"><h1>{h1}</h1><p>{sub}</p></div>'

