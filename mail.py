# ==================================================
# BIBLIOTECAS — Importação correta e completa
# ==================================================
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.header import decode_header
import time
import os
from dotenv import load_dotenv

# ✅ Notificação nativa do Windows — versão corrigida!
from windows_toasts import Toast, WindowsToaster

# ==================================================
# CARREGAR CONFIGURAÇÕES
# ==================================================
load_dotenv()

# ==================================================
# DADOS DE ACESSO — SEM espaços na senha!
# ==================================================
EMAIL = os.getenv("SEU_EMAIL", "ronaldodias.ti@gmail.com")
SENHA = os.getenv("SENHA_APP", "vywxmnidqxlsudqi")

IMAP_SERVIDOR = "imap.gmail.com"
IMAP_PORTA = 993
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587

CATEGORIA_ALVO = "concurso"

CAIXAS_PARA_BUSCAR = [
    "INBOX",              # 📥 Caixa de Entrada
    "[Gmail]/Spam",       # 🚫 Spam
    "[Gmail]/Lixeira"     # 🗑️ Lixeira
]

CRITERIOS_FILTRO = {
    "assunto_contem": ["riosaude"],
    "remetente_contem": ["concursos@", "pss.riosaude@", "riosaude@"],
    "corpo_contem": ["candidato"]
}

EMAIL_DESTINO_NOTIFICACAO = "ronaldodias.ti@gmail.com"
INTERVALO_VERIFICACAO = 60

# Inicializa notificação do Windows
notificador = WindowsToaster("Monitor de Concursos")

# ==================================================
# FUNÇÃO 1 → Aviso na TELA do Windows 🪟
# ==================================================
def avisar_na_tela(assunto, remetente):
    """Exibe notificação na barra do Windows — canto inferior direito"""
    try:
        aviso = Toast()
        aviso.text_fields = [
            "🔔 NOVO E-MAIL DE CONCURSO!",
            f"Assunto: {assunto[:60]}",
            f"De: {remetente[:40]}"
        ]
        notificador.show_toast(aviso)
        print("🪟 Notificação exibida na tela do Windows!")
        return True
    except Exception as erro:
        print(f"⚠️ Erro na notificação da tela: {erro}")
        return False

# ==================================================
# FUNÇÃO 2 → Aviso por E-MAIL 📩
# ==================================================
"""def enviar_aviso_email(assunto, remetente):
    try:
        texto = f"""
#🔔 NOVO E-MAIL DE CONCURSO DETECTADO!

#📌 Assunto: {assunto}
#👤 Remetente: {remetente}
#🕐 Hora: {time.strftime('%d/%m/%Y %H:%M:%S')}

#✅ Arquivado na pasta: {CATEGORIA_ALVO}
"""
        mensagem = MIMEText(texto, "plain", "utf-8")
        mensagem["Subject"] = "🔔 AVISO: Novo Concurso"
        mensagem["From"] = EMAIL
        mensagem["To"] = EMAIL_DESTINO_NOTIFICACAO

        with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
            servidor.starttls()
            servidor.login(EMAIL, SENHA)
            servidor.send_message(mensagem)

        print(f"📩 Aviso enviado por e-mail → {EMAIL_DESTINO_NOTIFICACAO}")
        return True
    except Exception as erro:
        print(f"⚠️ Erro ao enviar e-mail: {erro}")
        return False
"""
# ==================================================
# FUNÇÃO 3 → Decodificar acentuação ✅
# ==================================================
def decodificar_texto(texto):
    if not texto or not isinstance(texto, str):
        return ""
    try:
        partes = decode_header(texto)
        resultado = ""
        for conteudo, codificacao in partes:
            if isinstance(conteudo, bytes):
                resultado += conteudo.decode(codificacao or "utf-8", errors="replace")
            else:
                resultado += str(conteudo)
        return resultado
    except Exception:
        return str(texto)

# ==================================================
# FUNÇÃO 4 → Extrair corpo do e-mail 📄
# ==================================================
def extrair_corpo(mensagem):
    corpo = ""
    if mensagem.is_multipart():
        for parte in mensagem.walk():
            if parte.get_content_type() == "text/plain":
                try:
                    dados = parte.get_payload(decode=True)
                    if dados:
                        corpo += dados.decode("utf-8", errors="replace")
                except Exception:
                    continue
    else:
        try:
            dados = mensagem.get_payload(decode=True)
            if dados:
                corpo = dados.decode("utf-8", errors="replace")
        except Exception:
            corpo = ""
    return corpo

# ==================================================
# FUNÇÃO 5 → Verificar se é e-mail de concurso 🔍
# ==================================================
def e_concurso(assunto, remetente, corpo):
    assunto = assunto.lower()
    remetente = remetente.lower()
    corpo = corpo.lower()

    for palavra in CRITERIOS_FILTRO["assunto_contem"]:
        if palavra.lower() in assunto:
            return True
    for palavra in CRITERIOS_FILTRO["remetente_contem"]:
        if palavra.lower() in remetente:
            return True
    for palavra in CRITERIOS_FILTRO["corpo_contem"]:
        if palavra.lower() in corpo:
            return True
    return False

# ==================================================
# FUNÇÃO 6 → Buscar nas 3 caixas 📂
# ==================================================
def verificar_caixas(conexao, ids_ja_vistos):
    encontrados = 0
    for caixa in CAIXAS_PARA_BUSCAR:
        print(f"\n📂 Verificando: {caixa}")
        try:
            status, _ = conexao.select(caixa, readonly=True)
            if status != "OK":
                print(f"   ⚠️ Não foi possível acessar")
                continue

            status, dados = conexao.search(None, "ALL")
            if status != "OK":
                continue

            lista_ids = dados[0].split()
            print(f"   📩 {len(lista_ids)} e-mails encontrados")

            for id_email in reversed(lista_ids):
                if id_email in ids_ja_vistos:
                    continue
                ids_ja_vistos.add(id_email)

                status, dados = conexao.fetch(id_email, "(RFC822)")
                if status != "OK" or not dados or not dados[0]:
                    continue

                mensagem = email.message_from_bytes(dados[0][1])
                assunto = decodificar_texto(mensagem.get("Subject", ""))
                remetente = decodificar_texto(mensagem.get("From", ""))
                corpo = extrair_corpo(mensagem)

                if e_concurso(assunto, remetente, corpo):
                    print(f"   ✅ ENCONTRADO: {assunto} | De: {remetente}")
                    conexao.copy(id_email, CATEGORIA_ALVO)
                    avisar_na_tela(assunto, remetente)
                    enviar_aviso_email(assunto, remetente)
                    encontrados += 1
        except Exception as erro:
            print(f"   ❌ Erro: {type(erro).__name__}: {erro}")
    return encontrados

# ==================================================
# FUNÇÃO 7 → LOOP PRINCIPAL ♻️
# ==================================================
def main():
    ids_ja_vistos = set()
    print("=" * 60)
    print("🚀 MONITORAMENTO ATIVO — E-mails de Concurso")
    print("📥 Caixa de Entrada | 🚫 Spam | 🗑️ Lixeira")
    print("🪟 Notificação do Windows: ATIVADA")
    print(f"⏰ Verificação a cada {INTERVALO_VERIFICACAO} segundos")
    print("=" * 60)

    while True:
        conexao = None
        try:
            conexao = imaplib.IMAP4_SSL(IMAP_SERVIDOR, IMAP_PORTA)
            conexao.login(EMAIL, SENHA)
            print(f"\n✅ Conectado: {EMAIL}")

            _, pastas = conexao.list()
            nomes_pastas = []
            for p in pastas:
                if isinstance(p, bytes):
                    partes = p.decode().split('"')
                    if len(partes) >= 2:
                        nomes_pastas.append(partes[-2])

            if CATEGORIA_ALVO not in nomes_pastas:
                conexao.create(CATEGORIA_ALVO)
                print(f"📂 Pasta '{CATEGORIA_ALVO}' criada!")
            else:
                print(f"📂 Pasta '{CATEGORIA_ALVO}' pronta")

            novos = verificar_caixas(conexao, ids_ja_vistos)
            hora = time.strftime("%H:%M:%S")
            if novos == 0:
                print(f"✅ {hora} — Nenhum e-mail novo")
            else:
                print(f"✅ {hora} — {novos} e-mail(is) encontrado(s)")
        except Exception as erro:
            print(f"\n❌ Falha geral: {type(erro).__name__}: {erro}")
            print("🔄 Reconectando...")
        finally:
            if conexao:
                try:
                    conexao.logout()
                except:
                    pass
        time.sleep(INTERVALO_VERIFICACAO)

if __name__ == "__main__":
    main()