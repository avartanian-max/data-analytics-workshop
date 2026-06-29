# Step 1 — Load Data from CSV to DB

Read `climate_change_dataset.csv` and load it into the normalized schema,
mapping country strings to their lookup ids.

**Script:** `src/load.py`
**Run from:** project home

## Inputs & Outputs

| | Path |
|---|---|
| **Input** | `climate_change_dataset.csv` (1,000 rows) |
| **Schema** | `src/schema.sql` (executed by the loader) |
| **Output** | `climate_change.db` |

## Task

Create `src/load.py` that:

1. Deletes any existing `climate_change.db` (idempotent — clean rebuild every run).
2. Executes `src/schema.sql` to create tables.
3. Reads `climate_change_dataset.csv` with the `csv` module.
4. For each unique country string, inserts a row into `countries` and builds a
   `name → id` map.
5. For each CSV row, resolves the country string to its `country_id` and inserts
   one `climate_data` row.
6. All inserts run as parameterized statements inside a single transaction.

CSV columns → DB columns mapping:

| CSV column | DB column |
|---|---|
| `Year` | `year` |
| `Country` | `country_id` (via lookup) |
| `Avg Temperature (°C)` | `avg_temperature_c` |
| `CO2 Emissions (Tons/Capita)` | `co2_emissions_tons_per_capita` |
| `Sea Level Rise (mm)` | `sea_level_rise_mm` |
| `Rainfall (mm)` | `rainfall_mm` |
| `Population` | `population` |
| `Renewable Energy (%)` | `renewable_energy_pct` |
| `Extreme Weather Events` | `extreme_weather_events` |
| `Forest Area (%)` | `forest_area_pct` |

## Run

```bash
python src/load.py
```

Expected output:

```
Loaded 1000 rows into climate_change.db
```

## Quick sanity check

```bash
sqlite3 climate_change.db "SELECT COUNT(*) FROM climate_data;"   # -> 1000
sqlite3 climate_change.db "SELECT COUNT(*) FROM countries;"      # -> number of unique countries
```

## Prerequisites

- Python 3 (standard library only — `sqlite3`, `csv`, `pathlib`)

## Next

→ [Step 2 — Verify](step2-verify.md)
