from posixpath import split
import subprocess
import requests
import socket
ip = requests.get('https://api.ipify.org').text
# Descobre o nome do host (computador)
hostname = socket.gethostname()
# Descobre o endereço IP associado ao host
ip_local = socket.gethostbyname(hostname)
#print(f"Public IP Address: {ip}")
print(f"Endereço IP local: {hostname} : {ip_local}")
scan = ip_local.split('.')
x = int(scan[3])
while x < 30:
   x = x + 1
   pc = subprocess.run(["ping", "-n", "1", f"{scan[0]}.{scan[1]}.{scan[2]}.{x}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   local = socket.gethostbyname(pc.args[-1])
   erro =subprocess.run("%errorlevel%", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   if erro == 0:
       
         print(f"Public IP Address: {ip}")
         print(f"Endereço IP local: {local} : {ip_local}")
   else:
       
       print(f"ip:{scan[0]}.{scan[1]}.{scan[2]}.{x} is down")

