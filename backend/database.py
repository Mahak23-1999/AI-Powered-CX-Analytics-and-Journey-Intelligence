import sqlite3

conn = sqlite3.connect("reviews.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review TEXT,
    sentiment TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")