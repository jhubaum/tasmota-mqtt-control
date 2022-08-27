# Remote controlling a Tasmota driven device with MQTT
This repo contains a small prototype to demonstrate how devices with Tasmota drivers can be remote controlled using a Cloud server and MQTT. The prototype contains a simple webpage with a button to toggle the devices power state and a second button that does the same, but changes its state dynamically based on the state of the IOT device. Achieving this involves three components:

- Device: An IOT device somewhere that is driven by Tasmota. Instead of using a real device in my testing, I wrote a script `device.py` that uses MQTT to implement parts of the protocol described in the [Tasmota documentation](https://tasmota.github.io/docs/MQTT/#examples) (the power commands in particular).
- Server: A website running somewhere in the cloud, represented by `server.py`. The server interacts with the device by publishing and subscribing to specific MQTT topics. It also offers a(rest) api interface as an abstraction over the actual MQTT topics.
- Client: The web interface a user sees while interacting with the Server. The client only communicates with the server and has no knowledge about how the communication between device and server works. It is implemented in `templates/control_panel.html`

# Setup
## Install dependencies and run server
```
# clone this repository
git clone https://github.com/jhubaum/tasmota-mqtt-control.git mqtt_control
cd mqtt_controll

# setup virtual env and install requirements. This repo was tested with python 3.9.1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# run server
python server.py
```
If everything worked correctly, the server should keep running and print a log starting with something akin to
```
 * Serving Flask app 'server'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
Visit the URL shown in the printed log to try out the prototype.

## Setup a device
If you want to try the prototype with a real device, follow the steps [described here](https://tasmota.github.io/docs/MQTT/#configure-mqtt-using-webui) to configure it. You can find the values needed for the configuration in [config.py](config.py). They will also be shown on the web page of your server instance.

If you don't have a real device at hand and have already followed the steps to install all requirements, you can also just run `device.py`.

# Known issues
During testing, the sending of MQTT messages was sometimes a bit spotty. This is most likely because I'm using a public MQTT broker for testing. The effect I noticed most often by that is that the initial request for the device state gets dropped, resulting in a disabled interactive button. If this happens, simply reload the page a few times or press the toggle button.
