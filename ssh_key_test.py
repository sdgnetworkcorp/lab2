import paramiko
from pathlib import Path

key_path = Path(r'C:/Users/sandy/.ssh/unifi_key')
print('key exists', key_path.exists())
key = paramiko.RSAKey.from_private_key_file(str(key_path))
print('key loaded', type(key))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('192.168.1.1', username='sgutierez', pkey=key, timeout=10)
    print('connected')
    ssh.close()
except Exception as e:
    print('error', repr(e))
