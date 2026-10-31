from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from pathlib import Path

device = {
    "device_type":"cisco_xe",
    "host":"10.10.20.48",
    "username": input("Username: "),
    "password": getpass()
}

Path("backups").mkdir(exist_ok=True)

with ConnectHandler(**device) as conn:
    hostname = conn.find_prompt().strip("#>")
    config = conn.send_command("show running-config")

stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
filename = f"backups/{hostname}_{stamp}.txt"
Path(filename).write_text(config)
print(f"Saved {filename}")