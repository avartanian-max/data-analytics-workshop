# Step 0 — Design Schema & Create Tables

Define a normalized relational schema and create all tables, including a
`countries` lookup table and the `climate_data` fact table.

**Script:** `src/schema.sql`
**Run from:** project home

## Goal

Translate the flat 10-column `climate_change_dataset.csv` into a normalized schema:

- **Primary key** — `climate_data.record_id` (auto-increment).
- **Foreign key** — `climate_data` references a `countries` lookup table so
  country names are a controlled vocabulary enforced by referential integrity.
- **Constraints** — `NOT NULL` on every column; `UNIQUE` on country name;
  `CHECK` on year (1900–2100), renewable_energy_pct (0–100), forest_area_pct (0–100),
  population (> 0).

## Tables to Create

| Table | Role | Key |
|---|---|---|
| `countries` | Lookup dimension for country names | `country_id` PK, `name` UNIQUE |
| `climate_data` | Fact table, one row per country/year observation | `record_id` PK, `country_id` FK |

## Task

Create `src/schema.sql` with the following:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS climate_data (
    record_id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    year                         INTEGER NOT NULL CHECK(year BETWEEN 1900 AND 2100),
    country_id                   INTEGER NOT NULL REFERENCES countries(country_id),
    avg_temperature_c            REAL    NOT NULL,
    co2_emissions_tons_per_capita REAL   NOT NULL CHECK(co2_emissions_tons_per_capita >= 0),
    sea_level_rise_mm            REAL    NOT NULL,
    rainfall_mm                  REAL    NOT NULL CHECK(rainfall_mm >= 0),
    population                   INTEGER NOT NULL CHECK(population > 0),
    renewable_energy_pct         REAL    NOT NULL CHECK(renewable_energy_pct BETWEEN 0 AND 100),
    extreme_weather_events       INTEGER NOT NULL CHECK(extreme_weather_events >= 0),
    forest_area_pct              REAL    NOT NULL CHECK(forest_area_pct BETWEEN 0 AND 100)
);

CREATE INDEX IF NOT EXISTS idx_climate_country ON climate_data(country_id);
CREATE INDEX IF NOT EXISTS idx_climate_year    ON climate_data(year);
```

## Run

```bash
sqlite3 climate_change.db < src/schema.sql
```

## Verify

```bash
sqlite3 climate_change.db ".tables"
sqlite3 climate_change.db ".schema climate_data"
```

## Next

→ [Step 1 — Load CSV → DB](step1-load.md)
