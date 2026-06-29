# Step 2 — Verify

Confirm the loaded database is complete and referentially intact.

**Script:** `src/verify.sql`
**Run from:** project home

## Task

Create `src/verify.sql` with the checks below, then run it.

```sql
PRAGMA foreign_keys = ON;

-- Row counts
SELECT 'climate_data rows' AS check_name, COUNT(*) AS result FROM climate_data
UNION ALL
SELECT 'countries rows',                  COUNT(*)          FROM countries;

-- FK integrity
PRAGMA foreign_key_check;

-- No nulls in key columns
SELECT 'null years'       AS check_name, COUNT(*) AS result FROM climate_data WHERE year IS NULL
UNION ALL
SELECT 'null country_ids',               COUNT(*)           FROM climate_data WHERE country_id IS NULL
UNION ALL
SELECT 'null temperatures',              COUNT(*)           FROM climate_data WHERE avg_temperature_c IS NULL;

-- Year range
SELECT 'min year', MIN(year) FROM climate_data
UNION ALL
SELECT 'max year', MAX(year) FROM climate_data;

-- Renewable energy bounds (should all be 0–100)
SELECT 'out-of-range renewable_pct', COUNT(*)
FROM climate_data
WHERE renewable_energy_pct < 0 OR renewable_energy_pct > 100;

-- Forest area bounds (should all be 0–100)
SELECT 'out-of-range forest_area_pct', COUNT(*)
FROM climate_data
WHERE forest_area_pct < 0 OR forest_area_pct > 100;

-- Sample join to confirm country names resolve correctly
SELECT c.name, COUNT(*) AS observations
FROM climate_data cd
JOIN countries c ON cd.country_id = c.country_id
GROUP BY c.name
ORDER BY observations DESC
LIMIT 10;
```

## Run

```bash
sqlite3 climate_change.db < src/verify.sql
```

## Expected results

| Check | Expected |
|---|---|
| `climate_data rows` | 1000 |
| `countries rows` | number of unique countries in CSV |
| `PRAGMA foreign_key_check` | no rows (no FK violations) |
| `null *` checks | all 0 |
| `out-of-range *` checks | all 0 |

## Cross-check against CSV

```bash
# Count unique countries in the original CSV
tail -n +2 climate_change_dataset.csv | cut -d',' -f2 | sort -u | wc -l
```

## Previous

← [Step 1 — Load CSV → DB](step1-load.md)
