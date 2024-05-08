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
        
        # Inicializar o índice da notícia atual com 1
        self.indice_noticia_atual = 1
        
        # Conectar o botão ao método btnProximo
        self.btn_Proximo.clicked.connect(self.btnProximo)

        # Gerar os cards de notícias e exibir a primeira notícia
        self.listaDeCards = self.gerarCardsDeNoticias()
        self.exibirNoticiaAtual()
        
        # Conectar o botão para abrir o link da notícia
        self.btnLink.clicked.connect(self.abrirLink)

        # deixa a interface(propria do qt) transparerente
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
        cards = {} 
        for indice, card in enumerate(self.get_noticias()):
            titulo, resumo, link = self.get_detalhes_noticia(card)
            cards[indice+1] = (titulo, resumo, link)
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
        texto = card.find_all('div', class_= 'feed-post-body-resumo')[0]
        resumo = ''
        for linha in texto:
            resumo += linha.text
        return resumo
    
    # Exibir a notícia atual no aplicativo
    def exibirNoticiaAtual(self):
        noticia_atual = self.listaDeCards[self.indice_noticia_atual]
        titulo, resumo, link = noticia_atual
        self.set_titulo(titulo)
        self.set_resumo(resumo)
        self.set_link(link)
        
    # Atualizar a exibição para a próxima notícia
    def btnProximo(self):
        self.indice_noticia_atual += 1
        if self.indice_noticia_atual <= len(self.listaDeCards):
            self.exibirNoticiaAtual()
        else:
            QMessageBox.information(self, "Fim das notícias", "Não há mais notícias disponíveis.")
            self.indice_noticia_atual = 1
            self.clear_noticias()
            

    # Métodos para definir o título, resumo e link no aplicativo
    def set_titulo(self, titulo):
        self.btnTitulo.setText(titulo)

    def set_resumo(self, resumo):
        self.btnResumo.setText(resumo)

    def set_link(self, link):
        self.btnLink.setText("Acessar notícia")
        self.link_noticia = link
        
    # Método para abrir o link da notícia
    def abrirLink(self):
        if hasattr(self, 'link_noticia'):
            QDesktopServices.openUrl(QUrl(self.link_noticia))

    def clear_noticias(self):
        self.btnResumo.clear()
        self.btnTitulo.clear() 

if __name__ == '__main__':
    app = QApplication([])
    window = MeuApp()
    window.show()
    app.exec_()
