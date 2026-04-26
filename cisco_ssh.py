#!/usr/bin/env python3
"""
Network Device SSH Connection Script using Netmiko
This script connects to various network devices via SSH and allows executing commands.
"""

from netmiko import ConnectHandler
import paramiko
import getpass
import argparse
import os

def get_device_type():
    """Prompt user to select device type."""
    device_types = {
        '1': 'cisco_ios',      # Cisco IOS (routers, switches)
        '2': 'cisco_nxos',     # Cisco Nexus
        '3': 'cisco_asa',      # Cisco ASA Firewall
        '4': 'cisco_xe',       # Cisco IOS-XE
        '5': 'cisco_xr',       # Cisco IOS-XR
        '6': 'cisco_ios_telnet',  # Cisco IOS Telnet
        '7': 'cisco_wlc',      # Cisco Wireless LAN Controller
        '8': 'cisco_acios',    # Cisco ACI
        '9': 'cisco_ftd',      # Cisco Firepower Threat Defense
        '10': 'ubiquiti_edgerouter',  # Ubiquiti EdgeRouter
        '11': 'linux',         # Generic Linux/Unix devices (including some UniFi)
    }
    
    print("Select device type:")
    for key, value in device_types.items():
        print(f"{key}. {value}")
    
    while True:
        choice = input("Enter choice (1-11): ").strip()
        if choice in device_types:
            return device_types[choice]
        else:
            print("Invalid choice. Please select 1-11.")

def connect_linux(host, username, key_file=None, password=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    transport = paramiko.Transport((host, 22))
    transport.start_client(timeout=30)
    if key_file:
        try:
            pkey = paramiko.RSAKey.from_private_key_file(key_file)
        except Exception as e:
            transport.close()
            raise ValueError(f"Unable to load SSH key: {e}")
        try:
            transport.auth_publickey(username, pkey)
            ssh._transport = transport
            return ssh
        except paramiko.AuthenticationException:
            pass
    if password:
        try:
            transport.auth_interactive_dumb(username, lambda title, instructions, prompts: [password])
            ssh._transport = transport
            return ssh
        except paramiko.AuthenticationException:
            transport.close()
            raise
    transport.close()
    raise paramiko.AuthenticationException("Authentication failed using key and no password provided")


def main():
    parser = argparse.ArgumentParser(description="SSH to network devices")
    parser.add_argument('--host', required=True, help='Device IP/hostname')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', required=True, help='Password for authentication')
    parser.add_argument('--key-file', help='Private key file path')
    parser.add_argument('--device-type', help='Device type (will prompt if not provided)')
    
    args = parser.parse_args()
    
    host = args.host
    username = args.username
    password = args.password
    key_file_path = args.key_file
    device_type = args.device_type
    
    if not device_type:
        device_type = get_device_type()
    
    try:
        print(f"Connecting to {host} ({device_type})...")
        if device_type == 'linux':
            ssh = connect_linux(host, username, key_file_path if key_file_path else None, password)
            print("Connected successfully!")
            while True:
                command = input("Enter command (or 'exit' to quit): ")
                if command.lower() == 'exit':
                    break
                stdin, stdout, stderr = ssh.exec_command(command)
                print(stdout.read().decode(errors='ignore'))
                err = stderr.read().decode(errors='ignore')
                if err:
                    print(err)
            ssh.close()
            print("Disconnected.")
        else:
            device = {
                'device_type': device_type,
                'host': host,
                'username': username,
                'password': password,
                'use_keys': False,
                'allow_agent': False,
                'auth_timeout': 30,
            }
            net_connect = ConnectHandler(**device)
            if device_type in ['cisco_ios', 'cisco_xe', 'cisco_xr', 'cisco_wlc']:
                net_connect.enable()
            print("Connected successfully!")
            while True:
                command = input("Enter command (or 'exit' to quit): ")
                if command.lower() == 'exit':
                    break
                output = net_connect.send_command(command)
                print(output)
            net_connect.disconnect()
            print("Disconnected.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()