#!/usr/bin/env python3
import json
from marstek import MarstekClient

with open("config.json") as f:
    config = json.load(f)

client = MarstekClient(config["udp"]["ip"], config["udp"]["port"])

def show_status():
    try:
        print("\n=== ENERGY SYSTEM STATUS ===")
        es = client.es_get_status()
        print(f"Battery SOC: {es.get('bat_soc')}%")
        print(f"Battery Capacity: {es.get('bat_cap')} Wh")
        print(f"PV Power: {es.get('pv_power')} W")
        print(f"Grid Power: {es.get('ongrid_power')} W")
        print(f"Battery Power: {es.get('bat_power')} W")
        print(f"Load Power: {es.get('offgrid_power')} W")
        print(f"\nTotal PV Energy: {es.get('total_pv_energy')} Wh")
        print(f"Total Grid Output: {es.get('total_grid_output_energy')} Wh")
        print(f"Total Grid Input: {es.get('total_grid_input_energy')} Wh")
        print(f"Total Load Energy: {es.get('total_load_energy')} Wh")
        
        print("\n=== CURRENT MODE ===")
        mode = client.es_get_mode()
        print(f"Mode: {mode.get('mode')}")
        print(f"Grid Power: {mode.get('ongrid_power')} W")
        print(f"Off-grid Power: {mode.get('offgrid_power')} W")
        print(f"SOC: {mode.get('bat_soc')}%")
    except Exception as e:
        print(f"Error getting status: {e}")

def menu():
    while True:
        print("\n" + "="*40)
        print("MARSTEK CONTROL PANEL")
        print("="*40)
        print("1. Show Status")
        print("2. Set Auto Mode")
        print("3. Set AI Mode")
        print("4. Set Manual Mode")
        print("5. Set Passive Mode")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            show_status()
        elif choice == "2":
            if client.es_set_mode_auto():
                print("✓ Auto mode activated")
            else:
                print("✗ Failed to set mode")
        elif choice == "3":
            if client.es_set_mode_ai():
                print("✓ AI mode activated")
            else:
                print("✗ Failed to set mode")
        elif choice == "4":
            start = input("Start time (HH:MM): ").strip()
            end = input("End time (HH:MM): ").strip()
            power = int(input("Power (W): ").strip())
            if client.es_set_mode_manual(start_time=start, end_time=end, power=power):
                print("✓ Manual mode activated")
            else:
                print("✗ Failed to set mode")
        elif choice == "5":
            power = int(input("Power (W): ").strip())
            cd_time = int(input("Countdown (seconds): ").strip())
            if client.es_set_mode_passive(power=power, cd_time=cd_time):
                print("✓ Passive mode activated")
            else:
                print("✗ Failed to set mode")
        elif choice == "0":
            break

try:
    menu()
finally:
    client.close()
