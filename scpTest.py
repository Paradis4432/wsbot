from paramiko import SSHClient
from scp import SCPClient
from dotenv import load_dotenv
import os 
load_dotenv()

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(os.getenv('SERVERIP'),username='root', password=os.getenv('SSHPASS'))

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

scp.put('wsbot/images/wsimg.jpg')


scp.close()