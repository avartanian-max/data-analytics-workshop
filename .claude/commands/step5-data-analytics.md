# Step 5 — Data Analytics: Update data-analysis.ipynb

Append Python code cells to `src/data-analysis.ipynb` that produce the full
analytics deliverables — graphs, statistical tests, and detailed comparisons —
for the climate change dataset.

**Target notebook:** `src/data-analysis.ipynb`
**Run from:** project home
**Prerequisites:**
- Steps 0–2 done (populated `climate_change.db`); Step 4 cells present so the
  denormalized `df` (1000 × 11) is already loaded.
- Python packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `scikit-learn`.

## Task

**Append** the cells below to `src/data-analysis.ipynb` after the existing Step 4
load cells. Do **not** remove existing cells. Keep the notebook valid `nbformat` 4.5.

---

### Section setup — analytics imports (code)
```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)

NUMERIC = ["avg_temperature_c", "co2_emissions_tons_per_capita",
           "sea_level_rise_mm", "rainfall_mm", "renewable_energy_pct",
           "extreme_weather_events", "forest_area_pct"]
print("Rows:", len(df), "| Columns:", list(df.columns))
df[NUMERIC].describe()
```

---

## Task 1 — Hypothesis Development

### Cell — Hypothesis Matrix (markdown)

| # | Question | H0 (null) | H1 (alternative) | Planned test |
|---|----------|-----------|-------------------|--------------|
| 1 | CO2 emissions vs avg temperature | No correlation (ρ=0) | Correlation exists (ρ≠0) | Pearson/Spearman |
| 2 | Renewable energy % vs CO2 emissions | No correlation | Negative correlation | Pearson/Spearman |
| 3 | Forest area % vs CO2 emissions | No correlation | Negative correlation | Pearson/Spearman |
| 4 | Sea level rise trend over years | No trend (slope=0) | Rising over time | Linear regression |
| 5 | Avg temperature trend over years | No trend | Rising over time | Linear regression |
| 6 | Extreme weather events vs temperature | No correlation | Positive correlation | Pearson/Spearman |
| 7 | CO2 emissions differ by country | Equal means across countries | At least one differs | One-way ANOVA |
| 8 | Renewable energy differs by country | Equal means | At least one differs | One-way ANOVA |
| 9 | High vs low renewable energy → CO2 | Equal means (split at median) | Means differ | Independent t-test |

### Cell — Hypothesis matrix as a DataFrame (code)
Build the same matrix as a `pd.DataFrame` named `hypotheses` and display it.

---

## Task 2 — Exploratory Data Analysis (Visualization Portfolio)

### Cell — Histograms (code)
Histograms for each column in `NUMERIC` in a grid layout, with titles and axis labels.

### Cell — Boxplots (code)
Boxplots of `co2_emissions_tons_per_capita` and `avg_temperature_c` grouped by
`country` (top 10 countries by observation count). Use `sns.boxplot`; rotate x labels.

### Cell — Bar charts (code)
- Mean `co2_emissions_tons_per_capita` by country (top 15).
- Mean `renewable_energy_pct` by country (top 15).
- Total `extreme_weather_events` by country (top 15).

### Cell — Time-series line charts (code)
- Global mean `avg_temperature_c` per year.
- Global mean `sea_level_rise_mm` per year.
- Global mean `co2_emissions_tons_per_capita` per year.
- Global mean `renewable_energy_pct` per year.
Plot all four as subplots with year on the x-axis.

### Cell — Scatterplots (code)
- `co2_emissions_tons_per_capita` vs `avg_temperature_c`
- `renewable_energy_pct` vs `co2_emissions_tons_per_capita`
- `forest_area_pct` vs `co2_emissions_tons_per_capita`
- `extreme_weather_events` vs `avg_temperature_c`
Add regression lines via `sns.regplot`.

### Cell — Correlation matrix + heatmap (code)
```python
corr = df[NUMERIC].corr(method="pearson")
plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True)
plt.title("Correlation Matrix — climate numeric features")
plt.tight_layout(); plt.show()
corr
```

### Cell — EDA deliverable (markdown)
Short notes on distribution shapes, visible trends over time, and the
strongest/weakest correlations observed.

---

## Task 3 — Segmentation Analysis (Segmentation Report)

### Cell — Rule-based segments (code)
- **Emissions tier**: `pd.cut` of `co2_emissions_tons_per_capita` into Low/Medium/High.
- **Renewable tier**: `pd.cut` of `renewable_energy_pct` into Low/Medium/High.
- **Climate risk score**: combine standardized `avg_temperature_c` + `sea_level_rise_mm`
  + `extreme_weather_events` into a single risk score; bin into Low/Moderate/High/Severe.
- Show `groupby` mean scores and counts per segment.

### Cell — KMeans clustering (code)
Standardize `NUMERIC` with `StandardScaler`, fit `KMeans` (k=4, fixed `random_state`),
attach `cluster` to `df`, profile clusters with `groupby("cluster")[NUMERIC].mean()`,
and plot a scatter of `renewable_energy_pct` vs `co2_emissions_tons_per_capita`
colored by cluster.

### Cell — Segmentation deliverable (markdown)
Describe each segment/cluster: the type of country it represents and its
climate/emissions profile.

---

## Task 4 — Statistical Testing (Statistical Validation Report)

For every test: print the statistic, the p-value, and an explicit
**reject / fail-to-reject H0 at α = 0.05** decision.

### Cell — Correlation tests (code)
Pearson and Spearman for:
- `co2_emissions_tons_per_capita` vs `avg_temperature_c`
- `renewable_energy_pct` vs `co2_emissions_tons_per_capita`
- `forest_area_pct` vs `co2_emissions_tons_per_capita`
- `extreme_weather_events` vs `avg_temperature_c`
- `sea_level_rise_mm` vs `year`

### Cell — T-tests (code)
Split `df` at the median `renewable_energy_pct` into high/low groups.
Run `stats.ttest_ind` (Welch, `equal_var=False`) on:
- `co2_emissions_tons_per_capita`
- `avg_temperature_c`
- `extreme_weather_events`

### Cell — ANOVA (code)
`stats.f_oneway` across the top 10 countries by observation count for:
- `co2_emissions_tons_per_capita`
- `avg_temperature_c`
- `renewable_energy_pct`

### Cell — Linear regression / trend (code)
`stats.linregress` of `year` vs:
- `avg_temperature_c` (global annual mean)
- `sea_level_rise_mm` (global annual mean)

Print slope, intercept, r², and p-value; plot the regression line over the data.

### Cell — Confidence intervals (code)
95% CI on mean `co2_emissions_tons_per_capita` and `avg_temperature_c`
for high vs low renewable energy groups using `stats.t.interval` with group SEM.

### Cell — Statistical validation deliverable (code/markdown)
Collect each test's (statistic, p-value, decision) into a results DataFrame and
display it; add a markdown note tying results back to the Task 1 hypotheses.

---

## Task 5 — Preliminary Findings (markdown)

A summary cell covering:
- **Key findings** — strongest statistically supported relationships.
- **Significant relationships** — which H0 were rejected (with p-values).
- **Unexpected observations** — counter-intuitive or null results.
- **Policy / environmental implications** — actionable interpretation of the findings.

---

## Verify after update

- `src/data-analysis.ipynb` is valid `nbformat` 4.5 and the original Step 4 cells
  are intact.
- Run All executes top-to-bottom with no errors; every plot renders and every
  statistical test prints a decision.

## Previous

← [Step 4 — Create Notebook](step4-create-notebook.md)
