import paho.mqtt.client as mqtt 
import config

from flask import Flask, render_template

app = Flask(__name__)

client = mqtt.Client("Server Control")
client.connect(config.MQTT_BROKER) 

@app.route("/control/<cmd>", methods=["POST"])
def control_switch(cmd):
    if cmd in {"on", "off", "toggle"}:
        client.publish(f"cmnd/{config.TASMOTA_TOPIC}/POWER", cmd)
        return "Ok", 200
    return "Unknown command", 401

@app.route("/")
def home():
    return render_template('control_panel.html')

if __name__ == '__main__':
    app.run(debug=True)
