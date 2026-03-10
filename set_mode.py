#!/usr/bin/env python3
import sys
import json
from marstek import MarstekClient

with open("/home/bbeun/webserver/marstek/config.json") as f:
    config = json.load(f)

client = MarstekClient(config["udp"]["ip"], config["udp"]["port"])

mode = sys.argv[1].lower() if len(sys.argv) > 1 else "auto"

try:
    if mode == "auto":
        success = client.es_set_mode_auto()
    elif mode == "ai":
        success = client.es_set_mode_ai()
    elif mode == "manual":
        success = client.es_set_mode_manual()
    elif mode == "passive":
        power = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 3600
        success = client.es_set_mode_passive(power=power, cd_time=duration)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
    
    if success:
        print(f"Mode set to {mode}")
        sys.exit(0)
    else:
        print(f"Failed to set mode to {mode}")
        sys.exit(1)
finally:
    client.close()
