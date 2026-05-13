#!/usr/bin/env python3
import json
import time
import paho.mqtt.client as mqtt
from utils.config import Config
from utils.marstek import MarstekClient

# MQTT setup
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "MarstekPublisher")
mqtt_client.username_pw_set(Config.get("mqtt.user"), Config.get("mqtt.pass"))
mqtt_client.connect(Config.get("mqtt.broker"), Config.get("mqtt.port"), 60)
mqtt_client.loop_start()

# Marstek client
marstek = MarstekClient(Config.get("marstek.ip"), Config.get("marstek.port"))

def publish_all_keys():
    try:
        result = marstek.es_get_status()
        for key, value in result.items():
            topic = f"{Config.get('mqtt.prefix')}{key}"
            mqtt_client.publish(topic, value)
            print(f"{key} = {value} → gepusht naar {topic}", flush=True)
    except Exception as e:
        print("Fout bij ophalen/pushen:", e, flush=True)


while True:
    publish_all_keys()
    time.sleep(Config.get("marstek.polling_interval"))
