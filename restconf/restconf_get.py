import requests
from getpass import getpass
import urllib3

urllib3.disable_warnings()

HOST = "10.10.20.48"
auth = (input("Username: "), getpass())
headers = {"Accept":"application/yang-data+json"}

# url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces"
# r = requests.get(url, auth=auth, headers=headers, verify=False)
# r.raise_for_status()

# for intf in r.json()["ietf-interfaces:interfaces"]["interface"]:
#     ip = intf.get("ietf-ip:ipv4", {}).get("address", [{}])[0].get("ip", "-")
#     print(intf["name"], ip, intf["enabled"])

url = f"https://{HOST}/restconf/data/Cisco-IOS-XE-native:native/hostname"
r = requests.get(url, auth=auth, headers=headers, verify=False)
print(r.json())