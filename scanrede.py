import socket
import ipaddress

nome = socket.gethostname()
ip = socket.gethostbyname(nome)
n1 = 1
n2 = 1
ip_rede = ip.split('.')
while n1 < 255:
   
   
   rede_ip = ip.split('/')
   ip_enco = str(f"{ip_rede[0]}.{ip_rede[1]}.{ip_rede[2]}.{n1}")
   ip=str(ipaddress.ip_network(ip_enco))
   
   
   try:
       nome_rede = socket.gethostbyaddr(rede_ip[0])
       print(f"{n2} - Nome do dispositivo: {nome_rede[0]} IP: {rede_ip[0]}")
       n2 +=1

   except socket.herror:
       pass
