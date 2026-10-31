from pathlib import Path
from nornir_netmiko.tasks import netmiko_send_command


def backup_config(task):
    result = task.run(
        task=netmiko_send_command, command_string="show running-config"
    )

    Path("backups").mkdir(exist_ok=True)

    with open(f"backups/{task.hostname}.txt", "w") as f:
        f.write_text(result.result)
    
    return f"Backup saved: backups/{task.hostname}.txt"