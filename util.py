from config import TASMOTA_TOPIC, MQTT_BROKER

def control_channel():
    return f"cmnd/{TASMOTA_TOPIC}/POWER"

def status_channel():
    return f"stat/{TASMOTA_TOPIC}/POWER"
