import sys
sys.path.insert(0, r'C:\Users\choud\Downloads\energy_dashboard_streamlit')

print("Testing data_loader...")
from data_loader import load_clean, COL, countries, world_agg, latest_year_country
df = load_clean()
print(f"  Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"  Countries: {df['Entity'].nunique()}, Years: {sorted(df['Year'].unique())[:3]}...{sorted(df['Year'].unique())[-3:]}")
print(f"  co2_mt sample: {df['co2_mt'].dropna().head(3).values}")

print("Testing world_agg...")
w = world_agg(df)
print(f"  World agg shape: {w.shape}")

print("Testing latest_year_country...")
lt = latest_year_country(df)
print(f"  Latest: {lt.shape}")

print("Testing theme...")
from theme import CSS, kpi, sec, insight, hero, COLORS
print(f"  Colors: {list(COLORS.keys())}")
print(f"  kpi() sample: {kpi('⚡','100%','test')[:40]}")

print("Testing sklearn...")
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
X = np.random.rand(50,3)
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
print(f"  KMeans OK: {km.labels_[:5]}")

print("\n✅ ALL TESTS PASSED - Ready to launch!")

