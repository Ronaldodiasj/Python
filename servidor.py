import socket
import ollama
# Configurações
HOST = '127.0.0.1'  # Endereço local (mesma máquina)
PORTA = 5000         # Porta (acima de 1024)

# Cria o socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))
servidor.listen(1)  # Aceita até 1 conexão pendente

print(f"✅ Servidor rodando em {HOST}:{PORTA}")
print("⏳ Aguardando conexão do cliente...")

# Aceita conexão
conexao, endereco = servidor.accept()
print(f"🔌 Conectado com {endereco}")

try:
    while True:
        # Recebe dados (máximo 1024 bytes)
        dados = conexao.recv(1024)
        if not dados:
            break  # Cliente fechou a conexão
        
        mensagem = dados.decode('utf-8')
        print(f"📩 Cliente: {mensagem}")
        
        # Responde ao cliente
        resposta = input("Digite sua resposta: ")
        conexao.sendall(resposta.encode('utf-8'))

except KeyboardInterrupt:
    print("\n⚠️ Encerrando servidor...")
finally:
    conexao.close()
    servidor.close()
    print("🔌 Conexões fechadas")