import os
from getpass import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result
from nb_utils import get_loopbacks

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

for host in nr.inventory.hosts.values():
    host.platform="ios"

loopbackConfig = get_loopbacks()
print_result(nr.run(task=napalm_configure, configuration=loopbackConfig, dry_run=False))

# print_result(nr.run(task=netmiko_send_command,
#                     command_string="show ip interface brief"))