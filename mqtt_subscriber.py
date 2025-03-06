import paho.mqtt.client as mqtt

# MQTT Broker settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/sensor/temperature"

# Callback function when a message is received
def on_message(client, userdata, message):
    print(f"Received: {message.payload.decode()}")

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Connect to MQTT broker and subscribe to topic
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)

print(f"Subscribed to MQTT topic: {MQTT_TOPIC}")
mqtt_client.loop_forever()  # Keep listening for messages
