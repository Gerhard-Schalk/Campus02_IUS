#!/usr/bin/python3
# send messages to an MQTT broker
# This example is based on the following example: https://forums.raspberrypi.com/viewtopic.php?t=287326

import time
import paho.mqtt.client as mqtt 	# https://pypi.org/project/paho-mqtt/#client
import signal
import ssl				# https://docs.python.org/3/library/ssl.html

def sighandler(signum, frame):
    print('Signal handler called with signal', signum)
    exit(0)

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+connack_string(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        exit(1)
    else:
        print("MQTT disconnected")
        
signal.signal(signal.SIGTERM, sighandler)
signal.signal(signal.SIGINT,  sighandler)

ssl.SSLContext.verify_mode = ssl.VerifyMode.CERT_OPTIONAL

mqtthost = "192.168.0.100"
mqttport = 8883
# the client_id must be unique among clients
mqttclient = mqtt.Client(client_id="test1",
                         clean_session=True,
                         userdata=None,
                         transport="tcp")

#mqttclient.username_pw_set("probes", password="abcdefg")
mqttclient.reconnect_delay_set(min_delay=1, max_delay=120)
mqttclient.tls_set(
    ca_certs='/home/pi/MQTT_Client/TLS/Certs/ca/ca.crt',
    certfile='/home/pi/MQTT_Client/TLS/Certs/client/client.crt',
    keyfile='/home/pi/MQTT_Client/TLS/Certs/client/client.key',
    tls_version=ssl.PROTOCOL_TLSv1_2
)

mqttclient.on_connect    = on_connect
mqttclient.on_disconnect = on_disconnect

mqttclient.connect(mqtthost, mqttport)
mqttclient.subscribe("TestTopic", qos=1)

i = 0
while True:
    i = i + 1
    msg = "Hello, World from Python!" + i
    mqttclient.publish("TestTopic", payload=msg)
    time.sleep(5)