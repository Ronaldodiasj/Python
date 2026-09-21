import socket

HOST = '127.0.0.1'  # Mesmo endereço do servidor
PORTA = 5000         # Mesma porta

# Cria o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
print("✅ Conectado ao servidor!")
print("Digite 'sair' para encerrar\n")

try:
    while True:
        mensagem = input("Você: ")
        if mensagem.lower() == 'sair':
            cliente.sendall(mensagem.encode('utf-8'))
            break
        
        cliente.sendall(mensagem.encode('utf-8'))
        
        # Recebe resposta
        resposta = cliente.recv(1024).decode('utf-8')
        print(f"📩 Servidor: {resposta}")

except KeyboardInterrupt:
    print("\n⚠️ Encerrando...")
finally:
    cliente.close()
    print("🔌 Desconectado")