from opcua import Server
from datetime import datetime
import random
import time

# Create an OPC-UA server instance
server = Server()

# Set endpoint URL (Change IP to your local IP if needed)
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

# Create a namespace for the server
namespace = "http://example.org/opcua"
idx = server.register_namespace(namespace)

# Create an object (e.g., "Machine1") in the address space
machine = server.nodes.objects.add_object(idx, "Machine1")

# Create a variable (e.g., "Temperature") in the object
temperature = machine.add_variable(idx, "Temperature", 25.0)  # Initial value: 25°C

# Enable the variable to be writable
temperature.set_writable()

# Start the OPC-UA server
server.start()
print("OPC-UA Server Started at opc.tcp://localhost:4840/freeopcua/server/")

try:
    while True:
        # Simulate temperature changes
        new_temp = random.uniform(20.0, 30.0)  # Random temperature between 20°C and 30°C
        timestamp = datetime.now()

        # Update the OPC-UA variable
        temperature.set_value(new_temp)
        print(f"[{timestamp}] Updated Temperature: {new_temp:.2f}°C")

        time.sleep(2)  # Update every 2 seconds

except KeyboardInterrupt:
    print("\nShutting down OPC-UA Server...")
    server.stop()
