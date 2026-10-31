from napalm import get_network_driver
from getpass import getpass

driver = get_network_driver("ios")
device = driver("10.10.20.48", input("Username: "), getpass())
device.open()

# device.load_merge_candidate(config="""
# interface Loopback300
# description Added by NAPALM
# ip address 10.30.1.1 255.255.255.255
# """)

# diff = device.compare_config()
# if diff:
#     print(diff)
#     if input("Commit? (y/n): ")=="y":
#         device.commit_config()
#         print("COmmitted.")
#     else:
#         device.discard_config()
#         print("Discarded.")
# else:
#     print("No changes needed.")

device.rollback()
device.close()
