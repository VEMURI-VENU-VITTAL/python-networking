import pynetbox
import os
from jinja2 import Template
from getpass import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nb = pynetbox.api(
    "https://demo.netbox.dev",
    token=os.environ["NB_TOKEN"]
)

nr = InitNornir(
    runner={"plugin":"threaded", "options":{"num_workers":10}},
    inventory={
        "plugin":"NetBoxInventory2",
        "options":{
            "nb_url":"https://demo.netbox.dev",
            "nb_token":os.environ["NB_TOKEN"],
            "filter_parameters":{"site":"dc-lab"}
        }
    }
)

nr.inventory.defaults.username = input("Username: ")
nr.inventory.defaults.password = getpass()

def get_loopbacks():
    dev = nb.dcim.devices.get(name="cat8kv")

    interfaces = nb.dcim.interfaces.filter(device_id=dev.id)
    interfaceDict = []
    for intf in interfaces:
        if(intf.name.startswith("Loopback")):
            ips = nb.ipam.ip_addresses.filter(interface_id=intf.id)
            for ip in ips:
                address = ip.address.split("/")[0]
                interfaceDict.append(
                    {
                        "interface":intf.name,
                        "ip":address
                    }
                )

    config = Template(open("templates/loopback.j2").read()).render(loopbacks=interfaceDict)
    return config

def updateSerialNumber():
    for host in nr.inventory.hosts.values():
        host.platform = "ios"
    result = nr.run(task=napalm_get, getters=["get_facts"])
    facts = None
    for host, multi_result in result.items():
        facts = multi_result[0].result["get_facts"]
        facts = facts
        print(f"Device: {host}")
        print(f"Serial Number: {facts.get('serial_number')}")

    dev = nb.dcim.devices.get(name="cat8kv")
    dev.serial = facts["serial_number"]
    dev.save()

updateSerialNumber()