import requests
from getpass import getpass
import urllib3
import yaml

urllib3.disable_warnings()
f = open("loopbacks.yaml")
data = yaml.safe_load(f)
print(data)
HOST = "10.10.20.48"
auth = (input("Username: "), getpass())
headers = {
    "Accept":"application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

for loopback in data["loopbacks"]:
    payload = {
        "ietf-interfaces:interface":{
            "name":f"Loopback{loopback.get("id")}",
            "description":loopback.get("description"),
            "type":"iana-if-type:softwareLoopback",
            "enabled":True,
            "ietf-ip:ipv4":{
                "address":[{"ip":loopback.get("ip"), "netmask":"255.255.255.255"}]
            }
        }
    }

    url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{loopback["id"]}"
    r = requests.put(url, auth=auth, headers=headers, json=payload, verify=False)
    print(r.status_code)
