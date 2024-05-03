import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('interface.ui', self)
        self.btnDescer.clicked.connect(self.btn_descer)

        self.listaDeCards = self.gerarCardsDeNoticias()
        noticia = self.listaDeCards[1]
        # print(self.set_titulo(noticia[0]))
        self.set_resumo(noticia[1]) 
    #pegando noticias
    
    def procura_site(self, tag, classe):
        url = 'https://ge.globo.com/futebol/futebol-internacional/futebol-espanhol/times/real-madrid/'
        requisicao  = requests.get(url)
        pagina = BeautifulSoup(requisicao.text, 'html.parser')
        lista_noticias = pagina.find_all(tag, class_= classe)
        return lista_noticias
    
    def gerarCardsDeNoticias(self):
        cards = {} 
        for indice, card in enumerate(self.get_noticias()):
            titulo = self.get_titulo(card)
            resumo = self.get_resumo(card)
            cards[indice+1] = (titulo, resumo)
        return cards
    
    def get_noticias(self):
        return self.procura_site('div', 'feed-post-body')
    
    
    def get_titulo(self, card):
        # lista_noticias = card.find_all('a', class_= 'feed-post-link')
        titulo_link = card.find_all('a', class_= 'feed-post-link')[0]
        link = titulo_link.get('href')
        print(link)
        titulo = titulo_link.find_all('p')[0].getText()
        print(titulo)
        return titulo
    
    
    
    def get_resumo(self, card):
        texto = card.find_all('div', class_= 'feed-post-body-resumo')[0]
        resumo = ''
        for linha in texto:
            resumo += linha.text
        return resumo
    
    
    def set_titulo(self, titulo):
        self.btnTitulo.setText(titulo)

    def set_resumo(self, resumo):
        self.btnResumo.setText(resumo)

    def btn_descer(self):
        self.titulo = self.get_titulo()
        self.resumo = self.get_resumo()
        # print(self.titulo, self.resumo)


    
    
# lista_de_noticias = {}
 
# for indice, card in enumerate(get_noticias()):
#     titulo = get_titulo(card)
#     resumo = get_resumo(card)
#     lista_de_noticias[f'notica {indice+1}'] = (titulo, resumo)
   
 
 
 
 
# for noticia in lista_de_noticias:
#     notic = lista_de_noticias[noticia]
#     print(notic[0])
#     print(notic[1])
#     print()

if  __name__ == '__main__':
    app = QApplication([])
    window = MeuApp()
    window.show()
    app.exec_()

