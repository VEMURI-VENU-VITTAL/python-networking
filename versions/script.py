from netmiko import ConnectHandler
import yaml

with open("devices.yaml") as f:
    inventory = yaml.safe_load(f)

for device in inventory["devices"]:
    try:
        with ConnectHandler(**device) as conn:
            version_info = conn.send_command(
                "show version",
                use_textfsm=True
            )[0]

            print(f"version: {version_info['version']}")
            print(f"hostname: {version_info['hostname']}")
            print(f"serial number: {version_info['serial']}")
    except Exception as e:
        print(f"device: {device["device_type"]}, host name: {device["host"]} occurred error: {e}")