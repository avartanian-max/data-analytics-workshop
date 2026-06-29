# Step 4 — Create Notebook: Load climate_change.db → pandas DataFrame

Create a new Jupyter notebook that loads the SQLite database into pandas
DataFrames for analysis.

**Output notebook:** `src/data-analysis.ipynb`
**Run from:** project home
**Prerequisites:** Steps 0–2 completed (populated `climate_change.db` exists);
`pandas` and `jupyter` installed.

## Task

Create `src/data-analysis.ipynb` containing the cells below, in order.
Use `nbformat` 4.5. The `src/` directory already exists.

### Cell 1 — Markdown
```
# Step 4 — Load `climate_change.db` into pandas
Loads the normalized SQLite database into DataFrames. The denormalized frame
re-joins the countries lookup table to restore readable country names.
```

### Cell 2 — Imports & connect
```python
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path.cwd().parent / "climate_change.db" if Path.cwd().name == "src" \
          else Path.cwd() / "climate_change.db"
assert DB_PATH.exists(), f"climate_change.db not found at {DB_PATH} — run Steps 0–2 first"

conn = sqlite3.connect(DB_PATH)
```

### Cell 3 — List tables
```python
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn
)
tables
```

### Cell 4 — Load every table into a dict of DataFrames
```python
frames = {
    t: pd.read_sql(f"SELECT * FROM {t}", conn)
    for t in tables["name"]
}
{name: df.shape for name, df in frames.items()}
```

### Cell 5 — Denormalized analysis DataFrame
```python
df = pd.read_sql(
    """
    SELECT
        cd.record_id,
        cd.year,
        c.name                          AS country,
        cd.avg_temperature_c,
        cd.co2_emissions_tons_per_capita,
        cd.sea_level_rise_mm,
        cd.rainfall_mm,
        cd.population,
        cd.renewable_energy_pct,
        cd.extreme_weather_events,
        cd.forest_area_pct
    FROM climate_data cd
    JOIN countries c ON cd.country_id = c.country_id
    ORDER BY cd.year, c.name
    """,
    conn,
)
df.shape   # expect (1000, 11)
```

### Cell 6 — Peek
```python
df.head()
```

### Cell 7 — Structure & summary
```python
df.info()
df.describe(include="all")
```

### Cell 8 — Close connection
```python
conn.close()
```

## Verify after creation

- `src/data-analysis.ipynb` exists.
- Running all cells produces `df.shape == (1000, 11)` with no errors.

## Previous

← [Step 2 — Verify](step2-verify.md)
