import json
import logging
from scapy.all import *
import os
import pygame
import time

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("config.json not found , create file")
        exit(1)
    except json.JSONDecodeError:
        logging.error("Error decoding json file. Ensure proper format")
        exit(1)

def load_known_devices(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_known_device(filepath, mac_address):
    with open(filepath, "a") as f:
        f.write(mac_address + "\n")

def play_alert(sound_path):
    if not sound_path:
        logging.warning("No alert sound file found.")
        return
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception as e:
        logging.error(f"Could not play alarm sound: {e}")

def packet_handler(packet):
    global known_devices

    if packet.haslayer(DHCP) and packet[DHCP].options[0][1] == 3:
        try:
            mac_address = packet[Ether].src.lower()
            if mac_address not in known_devices:
                logging.info(f"New Device Detected : {mac_address}")
                known_devices.add(mac_address)
                save_known_device(config['known_devices_file'], mac_address)
                play_alert(config['alarm_sound_path'])
        except IndexError:
            pass
        except Exception as e:
            logging.error(f"An error occoured in packet handler: {e}")

if __name__ == "__main__":
    config = load_config()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    known_devices = load_known_devices(config['known_devices_file'])
    logging.info(f"Loaded {len(known_devices)} known devices.")
    logging.info("Starting network scan...")

    while True:
        try:
            sniff(prn=packet_handler, filter="udp and (port 67 or 68)", store=0)
        except Exception as e:
            logging.error(f"Sniffing failed: {e}. Restarting in 10 seconds...")
            time.sleep(10)
