from napalm import get_network_driver
from getpass import getpass
from pprint import pprint

driver = get_network_driver("ios")
device = driver("10.10.20.48", input("Username: "), getpass())

device.open()
pprint(device.get_facts())
pprint(device.get_interfaces_ip())
device.close()