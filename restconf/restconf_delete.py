import requests
from getpass import getpass
import urllib3

urllib3.disable_warnings()

HOST = "10.10.20.48"
auth = (input("Username: "), getpass())

headers = {
    "Accept":"application/yang-data+json",
    "Content-type":"application/yang-data+json"
}

payload = {
    "ietf-interfaces:interface":{
        "name":"Loopback200",
        "description":"Created via RESTCONF",
        "type":"iana-if-type:softwareLoopback",
        "enabled":True,
        "ietf-ip:ipv4":{
            "address":[{"ip":"10.200.1.1", "netmask":"255.255.255.255"}]
        }
    }
}

url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces/interface=Loopback200"
r = requests.delete(url, auth=auth, headers=headers, json=payload, verify=False)
print(r.status_code)