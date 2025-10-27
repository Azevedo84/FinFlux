from arquivos.chamar_arquivos import definir_caminho_arquivo
from comandos.notificacao import tratar_notificar_erros
from comandos.cores import cabecalho_tela, widgets, textos, fonte_botao, fundo_botao, widgets_escuro
from comandos.cores import fundo_tela, fundo_tela_menu
import os
import inspect

from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon

nome_arquivo_com_caminho = inspect.getframeinfo(inspect.currentframe()).filename
nome_arquivo = os.path.basename(nome_arquivo_com_caminho)


def icone(self, nome_imagem):
    try:
        camino = os.path.join('..', 'arquivos', 'icones', nome_imagem)
        caminho_arquivo = definir_caminho_arquivo(camino)

        self.setWindowIcon(QIcon(caminho_arquivo))

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def editar_botao(botao, nome_imagem, texto_botao, tamanho):
    try:
        layout = QVBoxLayout()
        layout.setSpacing(1)

        img_label = QLabel()
        camino = os.path.join('..', 'arquivos', 'icones', nome_imagem)
        caminho_imagem = definir_caminho_arquivo(camino)

        if not os.path.exists(caminho_imagem):
            print(f"Erro: A imagem {caminho_imagem} não foi encontrada.")
            return None

        icon = QPixmap(caminho_imagem)
        img_label.setPixmap(icon.scaled(QSize(tamanho, tamanho), aspectRatioMode=Qt.KeepAspectRatio))
        img_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(texto_botao)
        text_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(8)
        text_label.setFont(font)

        layout.addWidget(img_label)
        layout.addWidget(text_label)

        botao.setLayout(layout)

        # Ajustando o tamanho mínimo do botão
        botao.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def tamanho_aplicacao(self):
    try:
        monitor = QDesktopWidget().screenGeometry()
        monitor_width = monitor.width()
        monitor_height = monitor.height()

        if monitor_width > 1800 and monitor_height > 1024:
            interface_width = 1200
            interface_height = 675
        elif monitor_width > 1360 and monitor_height > 760:
            interface_width = 950
            interface_height = 534
        elif monitor_width > 1279 and monitor_height > 1020:
            interface_width = 1000
            interface_height = 562
        else:
            interface_width = int(monitor_width * 0.7)
            interface_height = int((interface_width / 16) * 9)

        x = (monitor_width - interface_width) // 2
        y = (monitor_height - interface_height) // 2

        self.setGeometry(x, y, interface_width, interface_height)


    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_widget_cab(nome_widget):
    try:
        nome_widget.setStyleSheet(f"background-color: {cabecalho_tela};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_widget(nome_widget):
    try:
        nome_widget.setStyleSheet(f"background-color: {widgets};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_widget_escuro(nome_widget):
    try:
        nome_widget.setStyleSheet(f"background-color: {widgets_escuro};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_fonte(nome_campo):
    try:
        nome_campo.setStyleSheet(f"color: {textos};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_btn(nome_botao):
    try:
        nome_botao.setStyleSheet(f"background-color: {fundo_botao}; color: {fonte_botao};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_fundo_tela(nome_widget):
    try:
        nome_widget.setStyleSheet(f"background-color: {fundo_tela};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)


def cor_fundo_tela_menu(nome_widget):
    try:
        nome_widget.setStyleSheet(f"background-color: {fundo_tela_menu};")

    except Exception as e:
        nome_funcao = inspect.currentframe().f_code.co_name
        tratar_notificar_erros(e, nome_funcao, nome_arquivo)
