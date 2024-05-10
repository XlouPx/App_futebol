import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from raspagem import Raspadura

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('interface.ui', self)

        # Objeto de Raspagem
        self.raspador = Raspadura()
        
        # Inicializar o índice da notícia atual com 0
        self.indice_noticia_atual = 0
        
        # Conectando o sinal clicked do botão ao método
        self.btnProximo.clicked.connect(self.btn_Proximo)
        self.btnAnterior.clicked.connect(self.btn_Anterior)
        self.btnFechar.clicked.connect(self.btn_Fechar)
        self.btnHistoria.clicked.connect(self.btn_Historia)
        self.btnHome.clicked.connect(self.btn_Home)
        self.btnJogadores.clicked.connect(self.btn_Jogadores) 
        self.btnNoticias.clicked.connect(self.btn_Noticias)

        # Gerar os cards de notícias e exibir a primeira notícia
        self.listaDeCards = self.raspador.gerarCardsDeNoticias()
        self.exibirNoticiaAtual()
        
        # Conectar o botão para abrir o link da notícia
        self.btnLink.clicked.connect(self.abrirLink)

        # Deixa a interface transparente
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

    # Função para fechar a janela
    def btn_Fechar(self):
        self.close()

    


    # Função para mostrar a história
    def btn_Historia(self):
        pass

    # Função para mostrar a página inicial
    def btn_Home(self):
        pass

    # Função para mostrar informações sobre os Melhores jogadores
    def btn_Jogadores(self):
        pass

    # Função para mostrar as notícias
    def btn_Noticias(self):
        pass
    

if __name__ == '__main__':
    app = QApplication([])
    window = MeuApp()
    window.show()
    app.exec_()
