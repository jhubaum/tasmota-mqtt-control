import paho.mqtt.client as mqtt 

import sys

import config

client = mqtt.Client("Server Control")
client.connect(config.MQTT_BROKER) 

client.publish(f"cmnd/{config.TASMOTA_TOPIC}/POWER", None if len(sys.argv) == 1 else sys.argv[1])
