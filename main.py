import requests
from os import path
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from raspagem import WebScraping


class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(self.localPath('interface.ui'), self)

        self.raspagem = WebScraping()
        self.indice_noticia_atual = 0
        self.conectar_botoes()
        self.lista_de_cards = self.gerar_cards_de_noticias()
        self.exibir_noticia_atual()
        self.show_home()

        self.btnLink.clicked.connect(self.abrir_link)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def localPath(self, relativo):
        return f'{path.dirname(path.realpath(__file__))}\\{relativo}'

    def conectar_botoes(self):
        # Conecta os botões aos métodos correspondentes
        botoes_metodos = {
            self.btnProximo: self.btn_proximo,
            self.btnAnterior: self.btn_anterior,
            self.btnVoltar: self.show_voltar,
            self.btnFechar: self.btn_fechar,
            self.btnHome: self.show_home,
            self.btnHistoria: self.show_historia,
            self.btnLerNoticias: self.show_ler_noticia,
            self.btnNoticia: self.show_noticias
        }

        for botao, metodo in botoes_metodos.items():
            botao.clicked.connect(metodo)

    def gerar_cards_de_noticias(self):
        # Gera os cards de notícias
        return self.raspagem.gerar_cards_de_noticias()

    def exibir_noticia_atual(self):
        # Exibe a notícia atual na interface
        noticia_atual = self.lista_de_cards[self.indice_noticia_atual]
        titulo, resumo, link = noticia_atual
        self.set_titulo(titulo)
        self.set_resumo(resumo)
        self.set_link(link)

    def btn_proximo(self):
        # Avança para a próxima notícia na lista
        self.indice_noticia_atual += 1
        if self.indice_noticia_atual < len(self.lista_de_cards):
            self.exibir_noticia_atual()
        else:
            self.indice_noticia_atual = 0

    def btn_anterior(self):
        # Retrocede para a notícia anterior na lista
        self.indice_noticia_atual -= 1
        if self.indice_noticia_atual >= 0:
            self.exibir_noticia_atual()
        else:
            self.indice_noticia_atual = len(self.lista_de_cards) - 1

    def exibir_noticia_completa(self):
        # Obtém a notícia completa
        noticia_completa = self.raspagem.get_noticias_full(self.link_noticia)
        self.btnLerNoticia.setText(noticia_completa)

    def set_titulo(self, titulo):
        # Define o título da notícia na interface
        self.btnTitulo.setText(titulo)

    def set_resumo(self, resumo):
        # Define o resumo da notícia na interface
        self.btnResumo.setText(resumo)

    def set_link(self, link):
        # Define o link da notícia na interface
        self.btnLink.setText("Acessar notícia")
        self.link_noticia = link

    def abrir_link(self):
        # Abre o link da notícia no navegador padrão
        if hasattr(self, 'link_noticia'):
            QDesktopServices.openUrl(QUrl(self.link_noticia))

    def btn_fechar(self):
        # Fecha a janela do aplicativo
        self.close()

    def show_home(self):
        # Exibe a página inicial na interface
        self.stackedWidget.setCurrentIndex(0)

    def show_historia(self):
        # Exibe a página de histórias na interface
        self.stackedWidget.setCurrentIndex(1)

    def show_ler_noticia(self):
        # Exibe a página para ler notícias na interface do método exibir a notícia completa
        self.stackedWidget.setCurrentIndex(2)
        self.exibir_noticia_completa()

    def show_noticias(self):
        # Exibe a página de notícias na interface
        self.stackedWidget.setCurrentIndex(3)

    def show_voltar(self):
        # Exibe a página de notícias na interface
        self.stackedWidget.setCurrentIndex(3)

if __name__ == '__main__':
    app = QApplication([])
    window = MeuApp()
    window.show()
    app.exec_()
