from paramiko import SSHClient
from scp import SCPClient
from dotenv import load_dotenv
import os
load_dotenv()

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(os.getenv('SERVERIP'), username='root',
            password=os.getenv('SSHPASS'))

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

cont = 0
subcont = 1
folder = input("folder name:")

i,o,e = ssh.exec_command(f"mkdir /root/wsbot/backup/{folder}")
if e.read():
    print(e.read())


scp.put(f"./images/img0.1.png",
        f"/root/wsbot/backup/{folder}/img{cont}.{subcont}.png")
ip = f"http://50.116.47.159/wsbot/backup/{folder}/img{cont}.{subcont}.png"
print(ip)

scp.close()
