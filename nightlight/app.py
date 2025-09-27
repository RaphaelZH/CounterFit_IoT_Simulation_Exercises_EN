import time

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

import paho.mqtt.client as mqtt

import json

CounterFitConnection.init("127.0.0.1", 5000)

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

id = "iot_001"
client_name = f"{id}_nightlight_client"
client_telemetry_topic = f"{id}_nightlight/telemetry"
server_command_topic = f"{id}_nightlight/commands/{id}"

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


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    light_level = light_sensor.light

    telemetry = json.dumps({"light_level": light_level})

    print("Sending telemetry: ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
