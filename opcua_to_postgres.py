from opcua import Client
import psycopg2
import time

# OPC-UA Server settings
OPC_SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="sensor_db",
    user="postgres",
    password="nmt",
    host="localhost",
    port="5433"
)
cursor = conn.cursor()

# Connect to OPC-UA Server
opcua_client = Client(OPC_SERVER_URL)
opcua_client.connect()
print(f"Connected to OPC-UA Server at {OPC_SERVER_URL}")

try:
    while True:
        # Read temperature value from OPC-UA
        temperature_node = opcua_client.get_node("ns=2;i=2")  # Adjust node ID if necessary
        temp_value = temperature_node.get_value()

        # Insert data into PostgreSQL
        cursor.execute("INSERT INTO temperature_data (temperature) VALUES (%s)", (temp_value,))
        conn.commit()

        print(f"Stored Temperature: {temp_value:.2f}°C in PostgreSQL")

        time.sleep(2)  # Insert every 2 seconds

except KeyboardInterrupt:
    print("\nShutting down...")
    opcua_client.disconnect()
    cursor.close()
    conn.close()
