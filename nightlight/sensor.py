import time

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

import paho.mqtt.client as mqtt

import json

CounterFitConnection.init("127.0.0.1", 5000)

light_sensor = GroveLightSensor(0)

id = "iot_001"
client_name = f"{id}/nightlight_client_1"
client_telemetry_topic = f"{id}/nightlight/telemetry"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_start()
print("MQTT connected!")

while True:
    light_level = light_sensor.light

    telemetry = json.dumps({"light_level": light_level})

    print("Sending telemetry: ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
