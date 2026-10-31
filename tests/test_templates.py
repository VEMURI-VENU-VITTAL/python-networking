import ipaddress
import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

def test_loopback_template_renders():
    out = env.get_template("loopback.j2").render(
        loopbacks=[{"id": 1, "ip": "10.0.0.1", "description": "test"}])
    assert "interface Loopback1" in out
    assert "ip address 10.0.0.1 255.255.255.255" in out

def test_inventory_data_is_valid():
    hosts = yaml.safe_load(open("inventory/hosts.yaml"))
    for name, host in hosts.items():
        ids = [lo["id"] for lo in host["data"]["loopbacks"]]
        assert len(ids) == len(set(ids)), f"{name}: duplicate loopback IDs"
        for lo in host["data"]["loopbacks"]:
            ipaddress.ip_address(lo["ip"])  # raises an error if the IP is invalid