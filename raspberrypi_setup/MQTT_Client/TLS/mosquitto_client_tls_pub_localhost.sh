#!/bin/bash
now=$(date +"%T")

mosquitto_pub -p 8883 \
  --cafile /home/pi/MQTT_Client/TLS/Certs/ca/ca.crt  \
  --cert /home/pi/MQTT_Client/TLS/Certs/client/client.crt \
  --key /home/pi/MQTT_Client/TLS/Certs/client/client.key \
  -h 192.168.0.100 \
  -t "TestTopic"  \
  -m "{\"Current time\" : \"$now\"}"
