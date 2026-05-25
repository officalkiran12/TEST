import sqlite3

COUNTRY_CODES = {
    'Nepal': 'NP',
    'United States': 'US',
    'India': 'IN',
    'Canada': 'CA',
    'Germany': 'DE',
    'Sweden': 'SE',
    'United Kingdom': 'GB',
    'Japan': 'JP',
    'Australia': 'AU',
    'Brazil': 'BR',
    'Global': 'GL',
}

conn = sqlite3.connect('jobs.db')
cur = conn.cursor()

for name, code in COUNTRY_CODES.items():
    cur.execute("UPDATE jobs SET country_code = ? WHERE country_name = ? AND (country_code IS NULL OR country_code = '')", (code, name))
    print(f"Updated {name} -> {code}: {cur.rowcount} rows")

# Also update country_code for jobs that have location-based country hints
cur.execute("UPDATE jobs SET country_code = 'NP' WHERE location LIKE '%Nepal%' AND country_code IS NULL")
print(f"Updated location-based Nepal: {cur.rowcount} rows")

conn.commit()
conn.close()
print("Done!")
