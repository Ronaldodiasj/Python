import socket
import ipaddress

nome = socket.gethostname()
ip = socket.gethostbyname(nome)
n4 = 0 
ip_rede = ip.split('.')
while n4 < 255:
   n4 +=1
   ip_enco =  str(f"{ip_rede[0]}.{ip_rede[1]}.{ip_rede[2]}.{n4}\0")
   ip=ipaddress.ip_network(ip_enco)
   nome_rede = socket.gethostbyaddr(ip)
   print(f"Nome do dispositivo: {nome_rede} IP: {ip}")