import time

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_led import GroveLed

import paho.mqtt.client as mqtt

import json

CounterFitConnection.init("127.0.0.1", 5000)

led = GroveLed(2)

id = "iot_001"
client_name = f"{id}/nightlight_client_3"
client_telemetry_topic = f"{id}/nightlight/telemetry"
server_command_topic = f"{id}/nightlight/commands/actuator_2"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_start()
print("MQTT connected!")


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload["led_on"]:
        led.on()
    else:
        led.off()


mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(5)
