# Network Sentry

## Description

Network Sentry is a Python-based network monitoring tool designed to detect and alert you to new devices connecting to your local network. It actively listens for DHCP requests and checks if the device's MAC address is already known. If a new device is detected, it logs the event, saves the new device's MAC address, and plays an audible alarm.

This tool is ideal for anyone who wants to keep an eye on their network's security and be notified of any unauthorized connections.

## Features

- **New Device Detection:** Monitors network traffic to identify new devices as they connect.
- **MAC Address Logging:** Keeps a persistent list of known devices for future reference.
- **Audible Alerts:** Plays a configurable alarm sound when a new device is detected.
- **Configuration File:** Uses a simple `config.json` file to manage settings.
- **Resilient Scanning:** Automatically restarts the network scan if it fails.

## Requirements

To run Network Sentry, you will need to have the following Python libraries installed:

- `scapy`: For packet sniffing and manipulation.
- `pygame`: For playing sounds.

You can install these dependencies using pip:

```bash
pip install scapy pygame
```

## Configuration

Before running the script, you need to create a `config.json` file in the same directory with the following structure:

```json
{
  "known_devices_file": "known_devices.txt",
  "alarm_sound_path": "path/to/your/alarm.mp3",
  "log_file": "network_sentry.log"
}
```

- `known_devices_file`: The path to the file where known MAC addresses will be stored.
- `alarm_sound_path`: The path to the sound file to be played when a new device is detected.
- `log_file`: The path to the file where logs will be stored.

## Usage

To start monitoring your network, simply run the script with root privileges:

```bash
sudo python3 sentry.py
```

The script needs to be run with `sudo` to allow `scapy` to capture network packets.

## How it Works

Network Sentry uses the `scapy` library to sniff for DHCP request packets on the network. These packets are typically sent by devices when they are trying to obtain an IP address from the DHCP server.

When a DHCP request is detected, the script extracts the source MAC address from the packet. It then checks if this MAC address is already present in the `known_devices_file`. If the MAC address is not found, the script considers it a new device and takes the following actions:

1.  Logs the detection of a new device, including its MAC address.
2.  Adds the new MAC address to the in-memory set of known devices.
3.  Appends the new MAC address to the `known_devices_file` for persistence.
4.  Plays the configured alarm sound to alert the user.
