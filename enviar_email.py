import os
import inspect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

import random


class EnvairEmail:
    def __init__(self):
        nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
        self.nome_arquivo = os.path.basename(nome_arquivo_com_caminho)

        self.email_user = 'ti.ahcmaq@gmail.com'
        self.password_old = 'poswxhqkeaacblku'
        self.password = "fsno grka ifsq jmzm"

        self.manipula_comeco()

    def dados_email(self):
        try:
            to = ['<azevedo.anderson@ymail.com>']

            current_time = (datetime.now())
            horario = current_time.strftime('%H')
            hora_int = int(horario)
            saudacao = ""
            if 4 < hora_int < 13:
                saudacao = "Bom Dia!"
            elif 12 < hora_int < 19:
                saudacao = "Boa Tarde!"
            elif hora_int > 18:
                saudacao = "Boa Noite!"
            elif hora_int < 5:
                saudacao = "Boa Noite!"

            msg_final = f"fudeu"

            return saudacao, msg_final, to

        except Exception as e:
            print(e)

    def envia_email(self):
        try:
            saudacao, msg_final, to  = self.dados_email()

            subject = f'OV - Separar material OV'

            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['Subject'] = subject

            body = f"{saudacao}\n\n" \
                   f"A está com todo mr separado.\n\n" \
                   f"{msg_final}"

            msg.attach(MIMEText(body, 'plain'))

            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_user, self.password)

            server.sendmail(self.email_user, to, text)

            server.quit()

            print(f'nviada com sucesso!')

        except Exception as e:
            print(e)

    def manipula_comeco(self):
        try:
            participantes = [
                ("Ana", "ana@email.com"),
                ("Bruno", "bruno@email.com"),
                ("Carla", "carla@email.com"),
                ("Diego", "diego@email.com"),
            ]

            nomes = [p[0] for p in participantes]
            resultado = self.derangement(nomes)

            for (nome, email), amigo in zip(participantes, resultado):
                msg = EmailMessage()
                msg["From"] = "Amigo Secreto <amigo@seudominio.com>"
                msg["To"] = email
                msg["Subject"] = "Seu Amigo Secreto 🎁"
                msg.set_content(
                    f"Olá {nome}!\n\n"
                    f"Seu amigo secreto é: 🎉 {amigo} 🎉\n\n"
                    "Guarde segredo 😉"
                )
                server.send_message(msg)

        except Exception as e:
            print(e)

    def derangement(self, lista):
        while True:
            sorteio = lista[:]
            random.shuffle(sorteio)
            if all(a != b for a, b in zip(lista, sorteio)):
                return sorteio


chama_classe = EnvairEmail()