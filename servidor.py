import socket
from ollama import chat

# Configurações
HOST = socket.gethonstname()  # Endereço local (mesma máquina)
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
        resposta = ollama.chat(model = "ollama3", messages=[{"role":"user", "content":"{dados}"}])
        if not dados:
            break  # Cliente fechou a conexão
        
        mensagem = dados.decode('utf-8')
        print(f"📩 Cliente: {mensagem}")
        
        # Responde ao cliente
        conexao.sendall(resposta.encode('utf-8'))
        print(resposta['messages']['content'])

except KeyboardInterrupt:
    print("\n⚠️ Encerrando servidor...")
finally:
    conexao.close()
    servidor.close()
    print("🔌 Conexões fechadas")