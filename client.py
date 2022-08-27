"""A script to simulate a voltage switch controller by TASMOTA


For details, look at the documentation: 
    https://tasmota.github.io/docs/MQTT/#examples
"""
import paho.mqtt.client as mqtt
import logging

from config import TASMOTA_TOPIC, MQTT_BROKER


enabled: bool = False

def on_message(client, userdata, message):
    global enabled

    message = message.payload.decode("utf-8")
    if message == "":
        print(f"Current state: {'Enabled' if enabled else 'Disabled'}")
    elif message == "on":
        enabled = True
        print("New state: Enabled")
    elif message == "off":
        enabled = False
        print("New state: Disabled")
    elif message == "toggle":
        enabled = not enabled
        print(f"New state: {'Enabled' if enabled else 'Disabled'}")
    else:
        logging.warning(f"Unknown message: {message}")
        return

    # Send info about state back.
    client.publish(f"stat/{TASMOTA_TOPIC}/POWER", "ON" if enabled else "OFF")


client = mqtt.Client("Power Switch")
client.connect(MQTT_BROKER) 

client.loop_start()

client.subscribe(f"cmnd/{TASMOTA_TOPIC}/POWER")
client.on_message=on_message 

print("Initialise: Disabled")

while True:
    # todo: catch kill signal for proper exit
    pass
