import os

import win32print
from win32com.client import Dispatch

texto = "Olá da impressora!\nEsse texto foi enviado direto pelo Python."

impressora = win32print.GetDefaultPrinter()
print(f"Impressora padrão: {impressora}")

impressao = Dispatch("Scripting.FileSystemObject")
arquivo = impressao.CreateTextFile("impressao.txt", True)
arquivo.Write(texto)
arquivo.Close()

os.system("notepad /p impressao.txt")
nome=os.system("hostname")