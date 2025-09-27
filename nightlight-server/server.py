import time

import paho.mqtt.client as mqtt

import json

id = "iot_001"
client_name = f"{id}/nightlight_server"
client_telemetry_topic = f"{id}/nightlight/telemetry"
server_command_topic_1 = f"{id}/nightlight/commands/actuator_1"
server_command_topic_2 = f"{id}/nightlight/commands/actuator_2"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_start()
print("MQTT connected!")


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = {"led_on": payload["light_level"] < 300}
    print("Sending command:", command)

    mqtt_client.publish(server_command_topic_1, json.dumps(command))
    mqtt_client.publish(server_command_topic_2, json.dumps(command))


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
