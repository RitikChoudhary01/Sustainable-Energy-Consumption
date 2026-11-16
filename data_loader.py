"""
Data loader and preprocessing for the Global Sustainable Energy dataset.
Source: Our World in Data / Kaggle — global-data-on-sustainable-energy.csv
"""

import os
import pandas as pd
import numpy as np

CSV_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "cleaned_sustainable_energy.csv"),
    os.path.join(os.path.dirname(__file__), "global-data-on-sustainable-energy.csv"),
    os.path.join(os.path.dirname(__file__), "energy_dashboard_streamlit", "cleaned_sustainable_energy.csv"),
    os.path.join(os.path.dirname(__file__), "energy_dashboard_streamlit", "global-data-on-sustainable-energy.csv"),
]
CSV_PATH = next((p for p in CSV_CANDIDATES if os.path.exists(p)), CSV_CANDIDATES[1])

# Short column aliases used throughout the app
COL = {
    "entity":       "Entity",
    "year":         "Year",
    "elec_access":  "Access to electricity (% of population)",
    "clean_fuels":  "Access to clean fuels for cooking",
    "renew_cap":    "Renewable-electricity-generating-capacity-per-capita",
    "fin_flows":    "Financial flows to developing countries (US $)",
    "renew_share":  "Renewable energy share in the total final energy consumption (%)",
    "fossil_twh":   "Electricity from fossil fuels (TWh)",
    "nuclear_twh":  "Electricity from nuclear (TWh)",
    "renew_twh":    "Electricity from renewables (TWh)",
    "lowcarbon":    "Low-carbon electricity (% electricity)",
    "energy_pc":    "Primary energy consumption per capita (kWh/person)",
    "intensity":    "Energy intensity level of primary energy (MJ/$2017 PPP GDP)",
    "co2":          "Value_co2_emissions_kt_by_country",
    "renew_pct_pe": "Renewables (% equivalent primary energy)",
    "gdp_growth":   "gdp_growth",
    "gdp_pc":       "gdp_per_capita",
    "density":      "Density\\n(P/Km2)",
    "land":         "Land Area(Km2)",
    "lat":          "Latitude",
    "lon":          "Longitude",
}


def load_raw() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    if "country" in df.columns:
        rev_map = {
            "country": COL["entity"],
            "year": COL["year"],
            "access_elec": COL["elec_access"],
            "clean_fuels": COL["clean_fuels"],
            "renew_cap_pc": COL["renew_cap"],
            "fin_flows": COL["fin_flows"],
            "renew_share": COL["renew_share"],
            "fossil_twh": COL["fossil_twh"],
            "nuclear_twh": COL["nuclear_twh"],
            "renew_twh": COL["renew_twh"],
            "lowcarbon_pct": COL["lowcarbon"],
            "energy_pc": COL["energy_pc"],
            "intensity": COL["intensity"],
            "co2_kt": COL["co2"],
            "renew_pe_pct": COL["renew_pct_pe"],
            "gdp_growth": COL["gdp_growth"],
            "gdp_pc": COL["gdp_pc"],
            "density": COL["density"],
            "land_area": COL["land"],
            "latitude": COL["lat"],
            "longitude": COL["lon"]
        }
        df = df.rename(columns=rev_map)
    # Clean density column
    if COL["density"] in df.columns:
        df[COL["density"]] = pd.to_numeric(df[COL["density"]], errors="coerce")
    return df


def load_clean() -> pd.DataFrame:
    df = load_raw()
    # Computed columns
    df["total_electricity_twh"] = (
        df[COL["fossil_twh"]].fillna(0)
        + df[COL["nuclear_twh"]].fillna(0)
        + df[COL["renew_twh"]].fillna(0)
    )
    df["co2_mt"] = df[COL["co2"]] / 1_000  # kt → Mt
    df["renew_twh_share"] = np.where(
        df["total_electricity_twh"] > 0,
        df[COL["renew_twh"]] / df["total_electricity_twh"] * 100,
        np.nan,
    )
    # Exclude rows with zero total electricity (mostly missing)
    return df


def countries(df: pd.DataFrame) -> list:
    return sorted(df[COL["entity"]].unique())


def years(df: pd.DataFrame) -> list:
    return sorted(df[COL["year"]].unique())


def filter_df(df, selected_countries=None, year_range=None):
    out = df.copy()
    if selected_countries:
        out = out[out[COL["entity"]].isin(selected_countries)]
    if year_range:
        out = out[(out[COL["year"]] >= year_range[0]) & (out[COL["year"]] <= year_range[1])]
    return out


def world_agg(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to world totals per year."""
    num_cols = [
        COL["fossil_twh"], COL["nuclear_twh"], COL["renew_twh"],
        COL["co2"], "total_electricity_twh", "co2_mt",
        COL["fin_flows"],
    ]
    mean_cols = [
        COL["elec_access"], COL["clean_fuels"], COL["renew_share"],
        COL["lowcarbon"], COL["energy_pc"], COL["intensity"],
        COL["gdp_growth"], COL["gdp_pc"], COL["renew_pct_pe"],
        COL["renew_cap"], "renew_twh_share",
    ]
    agg_dict = {c: "sum" for c in num_cols if c in df.columns}
    agg_dict.update({c: "mean" for c in mean_cols if c in df.columns})
    return df.groupby(COL["year"]).agg(agg_dict).reset_index()


def latest_year_country(df: pd.DataFrame) -> pd.DataFrame:
    """One row per country, using its latest available year."""
    return df.sort_values(COL["year"]).groupby(COL["entity"]).last().reset_index()


def region_map():
    """Rough continent mapping for selected entities."""
    return {
        "Asia": ["China", "India", "Japan", "South Korea", "Indonesia", "Bangladesh",
                 "Vietnam", "Thailand", "Pakistan", "Philippines", "Malaysia",
                 "Myanmar", "Cambodia", "Nepal", "Sri Lanka", "Afghanistan"],
        "Europe": ["Germany", "France", "United Kingdom", "Italy", "Spain",
                   "Poland", "Sweden", "Norway", "Denmark", "Finland",
                   "Netherlands", "Belgium", "Austria", "Switzerland",
                   "Russia", "Ukraine", "Romania", "Greece", "Portugal"],
        "Americas": ["United States", "Canada", "Brazil", "Mexico", "Argentina",
                     "Colombia", "Chile", "Peru", "Venezuela", "Ecuador"],
        "Africa": ["Nigeria", "South Africa", "Ethiopia", "Egypt", "Kenya",
                   "Ghana", "Tanzania", "Morocco", "Algeria", "Angola",
                   "Sudan", "Uganda", "Mozambique", "Madagascar", "Cameroon"],
        "Oceania": ["Australia", "New Zealand", "Papua New Guinea"],
        "Middle East": ["Saudi Arabia", "Iran", "United Arab Emirates",
                        "Iraq", "Qatar", "Kuwait", "Israel", "Jordan"],
    }

