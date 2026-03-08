import random
import smtplib
from email.message import EmailMessage

participantes = [
    ("Anderson", "azevedo.anderson@ymail.com"),
    ("Lara", "laradeazevedo22@gmail.com"),
    ("Ivania", "ivania@immig.com.br"),
    ("Adriano", "apamaio@gmail.com"),
    ("Altamir", "altamir.azevedo@gmail.com"),
    ("Luiza", "luizapi.azevedo@gmail.com"),
]

def derangement(lista):
    while True:
        sorteio = lista[:]
        random.shuffle(sorteio)
        if all(a != b for a, b in zip(lista, sorteio)):
            return sorteio

nomes = [p[0] for p in participantes]
resultado = derangement(nomes)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "ti.ahcmaq@gmail.com"
SMTP_PASS = "fsno grka ifsq jmzm"

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASS)

for (nome, email), amigo in zip(participantes, resultado):
    msg = EmailMessage()
    msg["From"] = "Amigo Secreto <amigo@seudominio.com>"
    msg["To"] = email
    msg["Subject"] = "Seu Amigo Secreto 🎁 - Oficial!"
    msg.set_content(
        f"Olá {nome}!\n\n"
        f"Agora é pra valer!!\n\n"
        f"Seu amigo secreto é: 🎉 {amigo} 🎉\n\n"
        "Guarde segredo 😉"
    )
    server.send_message(msg)

server.quit()

# apaga tudo da memória
del resultado
