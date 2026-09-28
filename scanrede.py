import socket
import ipaddress
# Responsavel de coletar as informação da rede ip nome da maquina
nome = socket.gethostname()
ip = socket.gethostbyname(nome)

# separa o ip em parte
ip_rede  = ip.split('.')

#Variavel utilizado para fazer a contagem
ip_ativo = 1
ip_desativodo = 1
ip_count = 0

# loop com nome e o ip de cada maquina
while ip_count < 3:
   # ip encontrado   
   ip_enco = str(f"{ip_rede[0]}.{ip_rede[1]}.{ip_rede[2]}.{ip_count}")
   ip=str(ipaddress.ip_network(ip_enco))
   rede_ip = ip.split('/')
   ip_count += 1   
   try:
       
       # conta o ip valido
       nome_rede = socket.gethostbyaddr(rede_ip[0])
       rede_mac = socket.getservbyport(rede_ip[0])
       print(f"{ip_count} - Dispositivo Ativo: {nome_rede[0]} IP: {rede_ip[0]} MAC{rede_mac} {ip_ativo} de 255")
       ip_ativo = str(ip_ativo += 1)
         
   except socket.herror:
       #conta o ip não tem retorno
       print(f"{ip_count} - Dispositivo Inativo IP: {rede_ip[0]} Inativo: {ip_desativodo} de 255 ") 
       ip_desativodo += 1 
#Resultado final
print(f"Total maquina Ativa {ip_ativo}  total de 255 só os ativos {ip_ativo} ")