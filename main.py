import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('interface.ui', self)
        
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
        self.listaDeCards = self.gerarCardsDeNoticias()
        self.exibirNoticiaAtual()
        
        # Conectar o botão para abrir o link da notícia
        self.btnLink.clicked.connect(self.abrirLink)

        # Deixa a interface transparente
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
                              
    # Função para procurar notícias no site
    def procura_site(self, tag, classe):
        url = 'https://ge.globo.com/futebol/futebol-internacional/futebol-espanhol/times/real-madrid/'
        requisicao  = requests.get(url)
        pagina = BeautifulSoup(requisicao.text, 'html.parser')
        lista_noticias = pagina.find_all(tag, class_= classe)
        return lista_noticias
    
    # Gerar os cards de notícias
    def gerarCardsDeNoticias(self):
        cards = [] 
        for card in self.get_noticias():
            titulo, resumo, link = self.get_detalhes_noticia(card)
            cards.append((titulo, resumo, link))
        return cards
    
    # Obter notícias do site
    def get_noticias(self):
        return self.procura_site('div', 'feed-post-body')
    
    # Obter detalhes (título, resumo e link) de uma notícia
    def get_detalhes_noticia(self, card):
        titulo_link = card.find_all('a', class_= 'feed-post-link')[0]
        link = titulo_link.get('href')
        titulo = titulo_link.find_all('p')[0].getText()
        resumo = self.get_resumo(card)
        return titulo, resumo, link
    
    # Obter o resumo de uma notícia
    def get_resumo(self, card):
        texto = card.find_all('div', class_= 'feed-post-body-resumo')[0].text
        return texto
    
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
