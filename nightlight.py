import time

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

import paho.mqtt.client as mqtt

CounterFitConnection.init("127.0.0.1",5000)

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

id = "iot_"
client_name = f"{id}nightlight_client"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_start()
print("MQTT connected!")

while True:
    light_level = light_sensor.light
    if light_level < 300:
        led.on()
    else:
        led.off()
    print("Light Level: ", light_level)
    #CounterFitConnection.send_data("light_level", light_level)
    time.sleep(1)