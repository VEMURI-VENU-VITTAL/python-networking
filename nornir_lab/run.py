import argparse

from getpass import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from scripts.backup_config import backup_config

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

dryRun = not args.apply

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = input("Username: ")
nr.inventory.defaults.password = getpass()

print_result(nr.run(task=netmiko_send_command, command_string="show version | include uptime"))

def deploy_loopbacks(task):
    cfg = task.run(task=template_file, template="loopback.j2", path="templates", loopbacks=task.host["loopbacks"])

    task.run(task=napalm_configure, configuration=cfg.result, dry_run=dryRun)

lab = nr.filter(site="lab")
print_result(lab.run(task=backup_config))
print(dryRun)
print_result(lab.run(task=deploy_loopbacks))