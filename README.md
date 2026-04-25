# Network Device SSH Python Script

This is a Python script to connect to various network devices via SSH using the Netmiko library.

## Requirements

- Python 3.x
- Netmiko library (install with `pip install -r requirements.txt`)

## Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python cisco_ssh.py
   ```
   Or with command line arguments:
   ```
   python cisco_ssh.py --host 192.168.1.1 --username sgutierez --device-type linux
   ```
   (Device type will be prompted if not provided)

3. Run the script (no password needed with key auth):
   ```
   python cisco_ssh.py --device-type linux
   ```

4. Once connected, you can enter Cisco commands interactively.
   - Type commands appropriate for the device type
   - Type `exit` to disconnect and quit.

## Supported Device Types

- Cisco IOS (routers, switches)
- Cisco Nexus (NX-OS)
- Cisco ASA Firewall
- Cisco IOS-XE
- Cisco IOS-XR
- Cisco IOS Telnet (fallback)
- Cisco Wireless LAN Controller (WLC)
- Cisco ACI
- Cisco Firepower Threat Defense (FTD)
- Ubiquiti EdgeRouter
- Generic Linux/Unix devices (for UniFi and other SSH-enabled devices)

## SSH Key and Password Setup

The script can use either SSH public key authentication or keyboard-interactive password authentication.

### Public key auth
If you want to use the generated key, add this public key to your UniFi user account:

```text
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCnk/xdjSQpM8mDYMmNWcR4MnTvWldvF1UDnTtBi3P6BaMKGOzVfl+imzkS543SPYQm17gK5Gm/DLL3sXhZQ+1zF8J12TRmpRxpk5keWuXGX+skv16QZL6E6ArgHx5dQQGYP61rTHRbZIiuC1LDt3alpvDamU6TdtDYs0ocH1w9+1oyDaR/vDpwhvDm/0aF5jU67GwYHhMh8wxBu2WAQNlvM84JBJg0jDvi8Jc2bkmbTMNnawLXmjzvd6D/0H8lumE1EyUcDG5/dedSzE6BdmdOplflYWg+/rLzl9aM7D9HNYczdsGlIuVu7TaM6XV3T18gtdjgz1ircbXt0testHvGEi6FtkVzjtfIYRS21GD2PbipNVAvL63YjGC/xRADCFk0dpSvU9bljOwP+w6QuR74PsJsJ5tuzo3xBUdzdqPTcFqXAGsh/e99ZMd6N10vJcFrfkp/lKJDtDG14dNumDjcs1aQ/Kl1Su14SPtpyTsVWExW0tahTZ3a8JuKWMbAmPk= sandy@Sandy
```

Then run:
```bash
python cisco_ssh.py --device-type linux
```

### Keyboard-interactive password auth
If your UniFi device is configured to accept password login via keyboard-interactive, run:

```bash
python cisco_ssh.py --device-type linux --password your_password
```
