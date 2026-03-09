#!/usr/bin/env python3
import json
import time
import paho.mqtt.client as mqtt
from marstek import MarstekClient

# Load config
with open("config.json") as f:
    config = json.load(f)

# MQTT setup
mqtt_client = mqtt.Client("MarstekPublisher")
mqtt_client.username_pw_set(config["mqtt"]["user"], config["mqtt"]["pass"])
mqtt_client.connect(config["mqtt"]["broker"], config["mqtt"]["port"], 60)
mqtt_client.loop_start()

# Marstek client
marstek = MarstekClient(config["udp"]["ip"], config["udp"]["port"])

def publish_all_keys():
    try:
        result = marstek.es_get_status()
        for key, value in result.items():
            topic = f"{config['mqtt']['prefix']}{key}"
            mqtt_client.publish(topic, value)
            print(f"{key} = {value} → gepusht naar {topic}", flush=True)
    except Exception as e:
        print("Fout bij ophalen/pushen:", e, flush=True)


while True:
    publish_all_keys()
    time.sleep(config["polling_interval"])
