import sqlite3

conn = sqlite3.connect("analytics.db")
conn.executescript("""
CREATE TABLE IF NOT EXISTS sales_daily (
    date TEXT, region TEXT, category TEXT,
    revenue REAL, orders INTEGER
);
INSERT OR IGNORE INTO sales_daily VALUES
    ('2025-09-01','North','Electronics',125000.50,310),
    ('2025-09-01','South','Grocery',54000.00,820),
    ('2025-09-01','West','Fashion',40500.00,190),
    ('2025-09-02','North','Electronics',132500.00,332),
    ('2025-09-02','West','Fashion',45500.00,210),
    ('2025-09-02','East','Grocery',62000.00,870);
""")
conn.commit()
conn.close()
print("analytics.db created and seeded!")