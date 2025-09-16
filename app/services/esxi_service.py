import paramiko
import time
import os
from app.config import ESXI_HOST, ESXI_USER, ESXI_PASS, ESXI_DATASTORE


def run_ssh_command(ssh, command: str):
    """Run SSH command and block until it finishes."""
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        raise Exception(
            f"Command failed: {command}\nError: {stderr.read().decode()}"
        )
    return stdout.read().decode()


def backup_vm_esxi(vm_name: str) -> str:
    """
    Connects to ESXi via SSH, clones VM disks using vmkfstools,
    compresses the backup, downloads it locally, and returns local file path.
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_vm_name = vm_name.replace(" ", "_")

    source_vmdk = f"/vmfs/volumes/{ESXI_DATASTORE}/backups/{vm_name}.vmdk"
    backup_dir = f"/vmfs/volumes/{ESXI_DATASTORE}/backups2/{safe_vm_name}_{timestamp}"
    backup_vmdk = f"{backup_dir}/{safe_vm_name}.vmdk"
    remote_tar = f"{backup_dir}.tar.gz"
    local_tar = f"/tmp/{safe_vm_name}_{timestamp}.tar.gz"  # container-local

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ESXI_HOST, username=ESXI_USER, password=ESXI_PASS)

    # 1. Create backup directory on ESXi
    run_ssh_command(ssh, f"mkdir -p '{backup_dir}'")

    # 2. Clone VM disk (thin provisioned)
    run_ssh_command(
        ssh, f"vmkfstools -i '{source_vmdk}' '{backup_vmdk}' -d thin"
    )

    # 3. Compress into tar.gz on ESXi
    run_ssh_command(
        ssh, f"tar -czf '{remote_tar}' -C '{backup_dir}' ."
    )

    # 4. Download tar.gz into API container
    sftp = ssh.open_sftp()
    sftp.get(remote_tar, local_tar)
    sftp.close()

    ssh.close()

    # 5. Verify file exists locally
    if not os.path.exists(local_tar):
        raise FileNotFoundError(f"Backup file missing after download: {local_tar}")

    return local_tar
