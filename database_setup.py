import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("sensor_data.db")
cursor = conn.cursor()

# Create table for storing OPC-UA sensor data
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL
)
""")

conn.commit()
conn.close()
print("Database and table created successfully!")
