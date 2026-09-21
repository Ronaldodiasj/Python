import ollama

# Exemplo de logs de rede recebidos
logs = [
    "2026-09-16 08:01:00 - Outbound connection to known malicious IP 185.220.101.1",
    "2026-09-16 08:02:15 - Successful login from admin from internal IP 192.168.1.10",
    "2026-09-16 08:05:00 - 500 failed login attempts detected from IP 45.9.20.11"
]

prompt_sistema = (
    "Você é um assistente de SOC (Security Operations Center). "
    "Analise os logs fornecidos e liste apenas os eventos críticos ou suspeitos."
)

conteudo_logs = "\n".join(logs)

response = ollama.chat(model='llama3', messages=[
    {'role': 'system', 'content': prompt_sistema},
    {'role': 'user', 'content': f"Analise estes logs:\n{conteudo_logs}"}
])

print(response['message']['content'])