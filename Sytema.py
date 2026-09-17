import socket
import subprocess

import win32print

nome_pc = subprocess.run("hostname", capture_output=True, text=True, check=False).stdout.strip()
usuario = subprocess.run("whoami", capture_output=True, text=True, check=False).stdout.strip()
ip =  socket.gethostbyname(socket.gethostname())
impressora = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
cpu = subprocess.run("wmic cpu get name", capture_output=True, text=True, check=False).stdout.strip()
Disk = subprocess.run("wmic logicaldisk get size,freespace,caption", capture_output=True, text=True, check=False).stdout.strip()
print(f"Nome do computador: {nome_pc}")
print(f"Usuário: {usuario}")
print(f"IP: {ip}")
print(f"Impressora: {impressora}")
print(f"CPU: {cpu}")
print(f"HD: {Disk}")