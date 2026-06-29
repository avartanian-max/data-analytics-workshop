import sqlite3
import csv
import os

csv_file = "climate_change_dataset.csv"
db_file = "climate_change.db"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS climate_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        country TEXT,
        avg_temperature_c REAL,
        co2_emissions_tons_per_capita REAL,
        sea_level_rise_mm REAL,
        rainfall_mm REAL,
        population INTEGER,
        renewable_energy_pct REAL,
        extreme_weather_events INTEGER,
        forest_area_pct REAL
    )
""")

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            int(row["Year"]),
            row["Country"],
            float(row["Avg Temperature (°C)"]),
            float(row["CO2 Emissions (Tons/Capita)"]),
            float(row["Sea Level Rise (mm)"]),
            float(row["Rainfall (mm)"]),
            int(row["Population"]),
            float(row["Renewable Energy (%)"]),
            int(row["Extreme Weather Events"]),
            float(row["Forest Area (%)"]),
        )
        for row in reader
    ]

cursor.executemany("""
    INSERT INTO climate_data (
        year, country, avg_temperature_c, co2_emissions_tons_per_capita,
        sea_level_rise_mm, rainfall_mm, population, renewable_energy_pct,
        extreme_weather_events, forest_area_pct
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

conn.commit()
conn.close()

print(f"Created {db_file} with {len(rows)} rows.")
