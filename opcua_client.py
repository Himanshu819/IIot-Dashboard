from opcua import Client
import time

# Define the OPC-UA server endpoint
server_url = "opc.tcp://localhost:4840/freeopcua/server/"

# Create a client instance
client = Client(server_url)

try:
    client.connect()
    print(f"Connected to OPC-UA Server at {server_url}")

    while True:
        # Access the Temperature variable
        temperature_node = client.get_node("ns=2;i=2")  # Namespace=2, ID=2 (Check the server output for actual node ID)
        temp_value = temperature_node.get_value()

        print(f"Current Temperature: {temp_value:.2f}°C")

        time.sleep(2)  # Read every 2 seconds

except KeyboardInterrupt:
    print("\nDisconnecting from OPC-UA Server...")
    client.disconnect()
