import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

CounterFitConnection.init('127.0.0.1',5000)

light_sensor = GroveLightSensor(0)
while True:
    light_level = light_sensor.light
    print("Light Level: ", light_level)
    #CounterFitConnection.send_data("light_level", light_level)
    time.sleep(1)