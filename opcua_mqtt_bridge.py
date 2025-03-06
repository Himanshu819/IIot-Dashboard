#base code for sending temp data to the OPCUA client

'''
from opcua import Client
import paho.mqtt.client as mqtt
import time
import json

# OPC-UA Server settings
OPC_SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"

# MQTT Broker settings
MQTT_BROKER = "broker.hivemq.com"  # Use "localhost" if using a local Mosquitto broker
MQTT_PORT = 1883
MQTT_TOPIC = "factory/sensor/temperature"

# Initialize OPC-UA client
opcua_client = Client(OPC_SERVER_URL)
opcua_client.connect()
print(f"Connected to OPC-UA Server at {OPC_SERVER_URL}")

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
print(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")

try:
    while True:
        # Read temperature value from OPC-UA
        temperature_node = opcua_client.get_node("ns=2;i=2")  # Adjust the node ID as needed
        temp_value = temperature_node.get_value()

        # Create a JSON payload
        payload = json.dumps({"temperature": temp_value, "unit": "°C"})
        
        # Publish data to MQTT broker
        mqtt_client.publish(MQTT_TOPIC, payload)
        print(f"Published to MQTT: {payload}")

        time.sleep(2)  # Send data every 2 seconds

except KeyboardInterrupt:
    print("\nShutting down...")
    opcua_client.disconnect()
    mqtt_client.disconnect() '''

#Modified code to store data from OPC_UA in the DATABASE


from opcua import Client
import psycopg2
import time

# ✅ OPC-UA Server settings
OPC_SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"

# ✅ PostgreSQL Database Connection
try:
    conn = psycopg2.connect(
        dbname="sensor_db",
        user="postgres",
        password="nmt",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL database")

    # ✅ Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature FLOAT NOT NULL
        )
    """)
    conn.commit()
    print("✅ Table 'temperature_data' checked/created.")

except psycopg2.Error as e:
    print(f"❌ Database connection error: {e}")
    exit()

# ✅ Connect to OPC-UA Server
try:
    opcua_client = Client(OPC_SERVER_URL)
    opcua_client.connect()
    print(f"✅ Connected to OPC-UA Server at {OPC_SERVER_URL}")

except Exception as e:
    print(f"❌ OPC-UA connection error: {e}")
    exit()

try:
    while True:
        # ✅ Read temperature value from OPC-UA
        try:
            temperature_node = opcua_client.get_node("ns=2;i=2")  # Adjust node ID if necessary
            temp_value = temperature_node.get_value()

            # ✅ Insert data into PostgreSQL
            cursor.execute("INSERT INTO temperature_data (temperature) VALUES (%s)", (temp_value,))
            conn.commit()

            print(f"📊 Stored Temperature: {temp_value:.2f}°C in database")

        except Exception as e:
            print(f"❌ Error reading from OPC-UA: {e}")

        time.sleep(2)  # ✅ Insert every 2 seconds

except KeyboardInterrupt:
    print("\n🔴 Shutting down...")
    opcua_client.disconnect()
    conn.close()
    print("✅ Database connection closed.")

