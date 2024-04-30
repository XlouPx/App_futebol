import requests
from bs4 import BeautifulSoup
 
 
#pegando noticias
 
def procura_site(tag, classe):
    url = 'https://ge.globo.com/futebol/futebol-internacional/futebol-espanhol/times/real-madrid/'
    requisicao  = requests.get(url)
    pagina = BeautifulSoup(requisicao.text, 'html.parser')
    lista_noticias = pagina.find_all(tag, class_= classe)
    return lista_noticias
 
def get_noticias():
    return procura_site('div', 'feed-post-body')
 
 
def get_titulo(card):
    # lista_noticias = card.find_all('a', class_= 'feed-post-link')
    titulo_link = card.find_all('a', class_= 'feed-post-link')[0]
    titulo = titulo_link.find_all('p')[0]
    return titulo
 
 
 
def get_resumo(card):
    texto = card.find_all('div', class_= 'feed-post-body-resumo')[0]
    resumo = ''
    for linha in texto:
        resumo += linha.text
    return resumo
 
 
 
 
lista_de_noticias = {}
 
for indice, card in enumerate(get_noticias()):
    titulo = get_titulo(card)
    resumo = get_resumo(card)
    lista_de_noticias[f'notica {indice+1}'] = (titulo, resumo)
   
 
 
 
 
for noticia in lista_de_noticias:
    notic = lista_de_noticias[noticia]
    print(notic[0])
    print(notic[1])
    print()