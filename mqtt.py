#!/usr/bin/env python3
import socket
import json
import time
import paho.mqtt.client as mqtt

# Load config
with open("config.json") as f:
    config = json.load(f)

UDP_IP = config["udp"]["ip"]
UDP_PORT = config["udp"]["port"]
MQTT_BROKER = config["mqtt"]["broker"]
MQTT_PORT = config["mqtt"]["port"]
MQTT_USER = config["mqtt"]["user"]
MQTT_PASS = config["mqtt"]["pass"]
MQTT_PREFIX = config["mqtt"]["prefix"]
POLLING_INTERVAL = config["polling_interval"]

# -------------------------------
# MQTT setup
# -------------------------------
mqtt_client = mqtt.Client("MarstekPublisher")
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# -------------------------------
# UDP socket setup
# -------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

# -------------------------------
# Functie: vraag status op en publish naar MQTT
# -------------------------------
def publish_all_keys():
    request = {
        "id": 1,
        "method": "ES.GetStatus",
        "params": {"id": 0}
    }
    sock.sendto(json.dumps(request).encode(), (UDP_IP, UDP_PORT))
    try:
        data, addr = sock.recvfrom(2048)
        response = json.loads(data.decode())
        result = response.get("result", {})

        # Publish elk key-value paar direct naar MQTT
        for key, value in result.items():
            topic = f"{MQTT_PREFIX}{key}"
            mqtt_client.publish(topic, value)
            print(f"{key} = {value} → gepusht naar {topic}", flush=True)

    except socket.timeout:
        print("Geen antwoord van Marstek", flush=True)
    except Exception as e:
        print("Fout bij ophalen/pushen:", e, flush=True)

# -------------------------------
# Main loop
# -------------------------------
while True:
    publish_all_keys()
    time.sleep(POLLING_INTERVAL)
