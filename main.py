import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from raspagem import WebScraping

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('interface.ui', self)

        # Objeto de Raspagem
        self.raspagem = WebScraping()
        
        # Inicializar o índice da notícia atual com 0
        self.indice_noticia_atual = 0
        
        # Conectando o sinal clicked do botão ao método
        self.btnProximo.clicked.connect(self.btn_Proximo)
        self.btnAnterior.clicked.connect(self.btn_Anterior)
        self.btnFechar.clicked.connect(self.btn_Fechar)
        self.btnHome.clicked.connect(self.showHome)
        self.btnHistoria.clicked.connect(self.showHistoria)
        self.btnLerNoticias.clicked.connect(self.showLerNoticia)
        self.btnNoticia.clicked.connect(self.showNoticias)

        # Gerar os cards de notícias e exibir a primeira notícia
        self.listaDeCards = self.gerarCardsDeNoticias()
        self.exibirNoticiaAtual()
        
        # Conectar o botão para abrir o link da notícia
        self.btnLink.clicked.connect(self.abrirLink)

        # Deixa a interface (própria do Qt) transparente
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    # Exibir a notícia atual no aplicativo
    def exibirNoticiaAtual(self):
        noticia_atual = self.listaDeCards[self.indice_noticia_atual]
        titulo, resumo, link = noticia_atual
        self.setTitulo(titulo)  
        self.setResumo(resumo)  
        self.setLink(link)   
                                
    # Atualizar a exibição para a próxima notícia
    def btn_Proximo(self):
        self.indice_noticia_atual += 1
        if self.indice_noticia_atual < len(self.listaDeCards):
            self.exibirNoticiaAtual()
        else:
            self.indice_noticia_atual = 0

    # Volta a exibição para a notícia anterior
    def btn_Anterior(self):
        self.indice_noticia_atual -= 1
        if self.indice_noticia_atual >= 0:
            self.exibirNoticiaAtual()
        else:
            self.indice_noticia_atual = len(self.listaDeCards) - 1

    # Métodos para definir o título, resumo e link no aplicativo
    def setTitulo(self, titulo):  
        self.btnTitulo.setText(titulo)  

    def setResumo(self, resumo):  
        self.btnResumo.setText(resumo)  

    def setLink(self, link):  
        self.btnLink.setText("Acessar notícia")  
        self.link_noticia = link
        
    # Método para abrir o link da notícia
    def abrirLink(self):
        if hasattr(self, 'link_noticia'):
            QDesktopServices.openUrl(QUrl(self.link_noticia))

    # Função para mostrar as notícias
    def btnNoticias(self):
        texto = self.raspagem.get_noticiasFull(self.link_noticias)
    
    # Função para fechar a janela
    def btn_Fechar(self):
        self.close()

    def showHome(self):
        self.stackedWidget.setCurrentIndex(0)

    def showHistoria(self):
        self.stackedWidget.setCurrentIndex(1)

    def showLerNoticia(self):
        self.stackedWidget.setCurrentIndex(2)

    def showNoticias(self):
        self.stackedWidget.setCurrentIndex(3)

if __name__ == '__main__':
    app = QApplication([])
    window = MeuApp()
    window.show()
    app.exec_()
