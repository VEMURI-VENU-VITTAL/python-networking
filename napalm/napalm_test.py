from napalm import get_network_driver
from getpass import getpass
from pprint import pprint

driver = get_network_driver("ios")

device = driver("10.10.20.48", input("Username: "), getpass())

device.open()
pprint(device.get_arp_table())
pprint(device.get_lldp_neighbors())

device.close()