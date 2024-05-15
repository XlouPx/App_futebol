import requests
from bs4 import BeautifulSoup

class WebScraping:
    
    def procura_site(self, url, tag, classe):
        """
        Procura por notícias em um site, dado uma URL, tag e classe.
        """
        requisicao = requests.get(url)
        pagina = BeautifulSoup(requisicao.text, 'html.parser')
        lista_noticias = pagina.find_all(tag, class_=classe)
        return lista_noticias
    
    def gerar_cards_de_noticias(self):
        """
        Gera os cards de notícias no formato HTML a partir dos dados obtidos.
        """
        cards = [] 
        for card in self.get_noticias():
            titulo, resumo, link = self.get_detalhes_noticia(card)
            cards.append((titulo, resumo, link))
        return cards
    
    def get_noticias(self):
        """
        Obtém uma lista de elementos HTML correspondentes às notícias do site.
        """
        url = 'https://ge.globo.com/futebol/futebol-internacional/futebol-espanhol/times/real-madrid/'
        return self.procura_site(url, 'div', 'feed-post-body')
    
    def get_detalhes_noticia(self, card):
        """
        Obtém detalhes (título, resumo e link) de uma notícia a partir de um card HTML.
        """
        titulo_link = card.find_all('a', class_='feed-post-link')[0]
        link = titulo_link.get('href')
        titulo = titulo_link.find_all('p')[0].getText()
        resumo = self.get_resumo(card)
        return titulo, resumo, link
    
    def get_resumo(self, card):
        """
        Obtém o resumo de uma notícia a partir de um card HTML.
        """
        texto = card.find_all('div', class_='feed-post-body-resumo')[0].text
        return texto

    def get_noticias_full(self, url):
        """
        Obtém o texto completo de uma notícia, dado uma URL específica.
        """
        requisicao = requests.get(url)
        pagina = BeautifulSoup(requisicao.text, 'html.parser')
        textos = [p.get_text() for p in pagina.find_all('p', 'content-text__container')]
        textos = str(textos).replace('+', '\n-').replace("', '", "").replace("['","").replace("']","")
        return textos
