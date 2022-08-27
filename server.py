import config
import util

from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MQTT_BROKER_URL'] = config.MQTT_BROKER
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.1  # refresh time in seconds
mqtt = Mqtt(app)
socketio = SocketIO(app, logger=True, engineio_logger=True)

@mqtt.on_connect()
def handle_mqtt_connect(client, userdata, flags, rc):
    mqtt.subscribe(util.status_channel())

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global socketio
    message = message.payload.decode('utf-8')
    print("Received MQTT status update: ", message)
    socketio.emit('status-update', dict(Power=message))

@app.route("/control/<cmd>", methods=["POST"])
def control_switch(cmd):
    if cmd in {"on", "off", "toggle"}:
        print("Sending command")
        mqtt.publish(util.control_channel(), cmd)
        return "Ok", 200
    return "Unknown command", 401

@app.route("/")
def home():
    return render_template('control_panel.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
