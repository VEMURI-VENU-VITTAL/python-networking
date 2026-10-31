import sys
import yaml
from jinja2 import Template
from netmiko import ConnectHandler
from getpass import getpass

data = yaml.safe_load(open("loopbacks.yaml"))
config = Template(open("loopback.j2").read()).render(data)

print("Config to push:\n" + config)

if "--apply" not in sys.argv:
    print("Dry run only. Use --apply to push.")
    sys.exit()

device = {
    "device_type": "cisco_xe",
    "host": "10.10.20.48",
    "username": input("Username: "),
    "password": getpass(),
}

with ConnectHandler(**device) as conn:
    output = conn.send_config_set(config.splitlines())
    print(output)
    conn.save_config()
    print(conn.send_command("show ip interface brief | include Loopback"))