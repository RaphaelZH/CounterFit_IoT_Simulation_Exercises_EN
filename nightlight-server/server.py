import time

import paho.mqtt.client as mqtt

import json

import mysql.connector

id = "iot_001"
client_name = f"{id}/nightlight_server"
client_telemetry_topic = f"{id}/nightlight/telemetry"
server_command_topic_1 = f"{id}/nightlight/commands/actuator_1"
server_command_topic_2 = f"{id}/nightlight/commands/actuator_2"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect("test.mosquitto.org", 1883, 60)

mqtt_client.loop_start()
print("MQTT connected!")

mydb = mysql.connector.connect(
    host="localhost", user="root", password="Métronome", database="nightlight_db"
)

mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS light_records (datetime VARCHAR(255), light_level INT)"
)
# mycursor.execute("DROP TABLE IF EXISTS iot_devices")
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    command = {"led_on": payload["light_level"] < 300}
    print("Sending command:", command)

    mqtt_client.publish(server_command_topic_1, json.dumps(command))
    mqtt_client.publish(server_command_topic_2, json.dumps(command))

    sql = "INSERT INTO light_records (datetime, light_level) VALUES (%s, %s)"
    val = (time.strftime("%Y-%m-%d %H:%M:%S"), payload["light_level"])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
