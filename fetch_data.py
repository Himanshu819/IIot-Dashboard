import psycopg2
conn = psycopg2.connect(
    dbname="sensor_db",
    user="postgres",
    password="nmt",
    host="localhost",
    port="5433"
)
cursor = conn.cursor()

# Fetch last 10 records
cursor.execute("SELECT * FROM temperature_data ORDER BY timestamp DESC LIMIT 10")
rows = cursor.fetchall()

print("Last 10 Temperature Readings:")
for row in rows:
    print(row)

conn.close()
