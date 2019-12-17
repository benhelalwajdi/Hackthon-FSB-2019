#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time, threading, ssl, random
import json

# client, user and device details
serverUrl   = "127.0.0.1"
clientId    = "clientId-0290d9r5RG"
device_name = "My Python MQTT device"
tenant      = "<<tenant_ID>>"
username    = "<<username>>"
password    = "<<password>>"

receivedMessages = []

# display all incoming messages
def on_message(client, userdata, message):
    print("Received operation " + str(message.payload))
    if (message.payload.startswith("510")):
        print("Simulating device restart...")
        publish("testtopic/1xzqdz", "501,c8y_Restart");
        print("...restarting...")
        time.sleep(1)
        publish("testtopic/1xzqdz", "503,c8y_Restart");
        print("...done...")

# send temperature measurement
def sendMeasurements():
    try:
        print("Sending temperature measurement...")

        data = {}
        data['TemperateurCuisine'] = "21," + str(random.randint(10, 20))
        data['TemperateurSalon'] = "27," + str(random.randint(10, 20))
        data['TemperateurVoiture'] = "21," + str(random.randint(10, 20))

        json_data = json.dumps(data)

        publish("testtopic/1xzqdz", json_data)
        #"211," + str(random.randint(10, 20))
        thread = threading.Timer(7, sendMeasurements)
        thread.daemon=True
        thread.start()
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print("Received keyboard interrupt, quitting ...")

# publish a message
def publish(topic, message, waitForAck = False):
    mid = client.publish(topic, message, 2)[1]
    if (waitForAck):
        while mid not in receivedMessages:
            time.sleep(0.25)

def on_publish(client, userdata, mid):
    receivedMessages.append(mid)

# connect the client to Cumulocity and register a device
client = mqtt.Client(clientId)
client.username_pw_set(tenant + "/" + username, password)
client.on_message = on_message
client.on_publish = on_publish

client.connect(serverUrl)
client.loop_start()
publish("testtopic/1xzqdz", "100," + device_name + ",c8y_MQTTDevice", True)
publish("testtopic/1xzqdz", "110,S123456789,MQTT test model,Rev0.1")
publish("testtopic/1xzqdz", "114,c8y_Restart")
print("Device registered successfully!")

client.subscribe("s/ds")
sendMeasurements()
