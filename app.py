import time

import paho.mqtt.client as mqtt

import json

id = "iot_001_"
client_name = f"{id}nightlight_client"
client_telemetry_topic = f"{id}nightlight/telemetry"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_start()
print("MQTT connected!")

def handle_telemetry(msg):
    payload = json.loads(msg.payload.decode())
    print("Received telemetry: ", payload)
    mqtt_client.subscribe(client_telemetry_topic)
    mqtt_client.on_message = handle_telemetry

    while True:
        time.sleep(2)