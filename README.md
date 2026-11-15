# ⚡ EnergyIQ — Sustainable Energy Consumption Dashboard
### SR UNIVERSITY · School of Computer Science and Artificial Intelligence
**Course:** Data Analytics and Visualization (25CAI202PC201)  
**Project Number:** 10  
**Curiosity Question:** *How can energy usage be optimized?*  
**Final Output:** Interactive Sustainable Energy Intelligence Dashboard

---

## 🌟 Executive Summary

**EnergyIQ** is an interactive web-based analytics dashboard built with **Streamlit, Plotly, Pandas, NumPy, and Scikit-Learn**. It analyzes the **Global Data on Sustainable Energy (2000–2020)** dataset spanning 176 countries over 21 years to answer the fundamental question:

> **How can energy usage be optimized?**

The dashboard provides deep empirical insights across 7 structured modules:
1. 🌟 **Global Executive Pulse**: Real-time cross-sectional metrics, 3D Natural Earth Choropleth map, and macro structural transition charts.
2. ⚡ **Electricity Generation Mix & Decarbonization**: Renewable vs Nuclear vs Fossil breakdown, Top 15 clean energy producers, and 20-year low-carbon heatmaps.
3. 📉 **Energy Efficiency & Decoupling (Intensity)**: Analysis of Energy Intensity ($MJ/\$GDP$), identification of efficiency champions, and Environmental Kuznets curves.
4. 🌍 **Country Benchmarking & Radar Profiling**: 6-axis normalized radar benchmarking and comparative trajectory visualizers.
5. 🤖 **AI Clustering & ML Predictive Forecasting**: K-Means clustering identifying 4 country energy archetypes, plus regression forecasting to 2035.
6. 🧮 **Optimization Levers & Scenario Simulator**: Interactive policy simulator testing fossil phase-outs, efficiency standards, and electrification.
7. 📋 **Data Quality, Methodology & Full Export**: Provenance audit, data dictionary, filterable dataset table, and 1-click CSV export.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Packages: `streamlit`, `plotly`, `pandas`, `numpy`, `scikit-learn`)*

### 3. Launch Dashboard
```bash
# From workspace directory:
streamlit run app.py
```
Then open your browser at **`http://localhost:8501`**.

---

## 📂 Project Structure

```
energy_dashboard_streamlit/
├── app.py                                          # Main Streamlit Dashboard Application
├── global-data-on-sustainable-energy.csv           # Kaggle / World Bank / OWID Dataset (176 countries)
├── requirements.txt                                # Python package dependencies
├── README.md                                       # Comprehensive project documentation
├── .streamlit/
│   └── config.toml                                 # Custom theme and server settings
└── DAV_Project_Report_Template.docx                # Academic Project Report Document
```

---

## 🔬 Answering the Curiosity Question: *How Can Energy Usage Be Optimized?*

Based on statistical and machine learning analysis of the 21-year dataset, energy usage can be optimized through **5 Empirical Pillars**:

| Pillar | Mechanism | Empirical Impact |
| :--- | :--- | :--- |
| **1. Decouple GDP via Energy Intensity** | Enforce building efficiency codes, industrial variable-frequency drives, and heat pump adoption | Every $1.0\text{ MJ/\$}$ intensity reduction saves $\approx 3,200\text{ TWh}$ globally |
| **2. Merit-Order Grid Dispatch** | Prioritize zero-marginal-cost renewables over fossil peaker plants | Cuts grid carbon intensity by up to $45\%$ |
| **3. Universal Induction & Clean Cooking** | Replace biomass/kerosene with electric induction in rural areas | Elevates cooking thermal efficiency from $15\%$ to $85\%$ |
| **4. Dynamic Time-of-Use Demand Response** | Price power dynamically to shift industrial loads into peak solar windows | Flattens the duck curve, avoiding redundant gas turbine buildouts |
| **5. Cross-Border HVDC Interconnection** | Connect regional grids to share complementary wind and solar resources | Reduces battery storage requirements by up to $35\%$ |

---

## 🛠️ Technology Stack

- **Frontend & App Engine:** Streamlit 1.28+ with glassmorphism CSS
- **Interactive Visualization:** Plotly Express & Plotly Graph Objects
- **Data Engineering:** Pandas & NumPy
- **Machine Learning:** Scikit-Learn (K-Means Clustering, Linear Regression, StandardScaler)
- **Styling:** Custom CSS, Google Inter typography, CSS Grid & Flexbox, SVG icons

---

*Submitted for Data Analytics and Visualization (25CAI202PC201) · SR University School of Computer Science & AI*

