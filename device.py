"""A script to simulate a voltage switch controller by TASMOTA


For details, look at the documentation: 
    https://tasmota.github.io/docs/MQTT/#examples
"""
import logging
import time
import paho.mqtt.client as mqtt

import util
import config

enabled: bool = False
message_queue = []

def simulate_voltage_control(client, userdata, message):
    global enabled
    global message_queue

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

    message_queue.append("ON" if enabled else "OFF")

print("Initialise: Disabled")

client = mqtt.Client("Simulated Socket")
client.connect(config.MQTT_BROKER)
client.subscribe(util.control_channel())
client.on_message = simulate_voltage_control

client.loop_start()

try:
    while True:
        time.sleep(0.1)
        if len(message_queue) > 0:
            print("Sending status update")
            client.publish(util.status_channel(), message_queue.pop())
except KeyboardInterrupt:
    pass
