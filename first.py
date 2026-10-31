from netmiko import ConnectHandler
from getpass import getpass

device = {
    "device_type": "cisco_xe",
    "host": "10.10.20.48",   # device IP from your reservation
    "username": input("Username: "),
    "password": "C1sco12345",
    "session_log":"netmiko.log"
}

with ConnectHandler(**device) as conn:
    interfaces = conn.send_command("show ip interface brief", use_textfsm=True)
    for intf in interfaces:
        print(intf)