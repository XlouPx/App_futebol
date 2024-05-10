import requests
from bs4 import BeautifulSoup


class Raspadura:

    # Função para procurar notícias no site
    def procura_site(self, url, tag, classe):
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
        url = 'https://ge.globo.com/futebol/futebol-internacional/futebol-espanhol/times/real-madrid/'
        return self.procura_site(url, 'div', 'feed-post-body')
    
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
    
    # Função de web scrap da noticias inteira
    def get_noticiasFull(self, url):
        
        # url = "https://ge.globo.com/futebol/futebol-internacional/noticia/2024/05/09/tchouameni-tem-lesao-confirmada-e-vira-preocupacao-para-final-da-champions.ghtml"
        textos = self.procura_site(url, 'p', 'content-text__container')
        return textos
    
    

if __name__ == "__main__":
    raspador = Raspadura()
    listaDeCards = raspador.gerarCardsDeNoticias()
    noticia1 = listaDeCards[0]
    url = noticia1[2]
    full = raspador.get_noticiasFull(url)
    print(full)


    #news = raspador.get_detalhes_noticia()
    
    #print()
