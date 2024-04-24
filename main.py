from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QMessageBox
from PyQt5.uic import loadUi
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

class MeuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(self.localPath('interface.ui'), self)
        self.pushButton.clicked.connect(self.iniciar_raspagem)

    def localPath(self, relativo):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), relativo)

    def iniciar_raspagem(self):
        self.textBrowser.clear()
        self.textBrowser.append("Iniciando a Coleta de dados...")
        self.executar_raspagem()

    def executar_raspagem(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-minimized')

        try:
            # Criando e configurando o driver do Chrome
            driver = webdriver.Chrome(options=chrome_options)
            driver.minimize_window()
            driver.get('https://www.playscores.com/scanner-futebol-online/ao-vivo')
            driver.implicitly_wait(10)
            
            # Encontrando os elementos dos jogos
            elements = driver.find_elements(By.CSS_SELECTOR, 'app-fixture-list-line.ng-star-inserted')
            total_jogos = len(elements)

            # Processando as informações dos jogos
            dados = [self.processar_informacoes_jogo(jogo, indice) for indice, jogo in enumerate(elements, start=1)]
            self.mostrar_resultados(dados, total_jogos)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao iniciar a raspagem: {e}")
        finally:
            driver.quit()

    def processar_informacoes_jogo(self, jogo, indice):
        try:
            # Dividindo as linhas de informações do jogo
            linhas = jogo.text.split('\n')
            # Extraindo as informações relevantes
            inf = [linha.split(':')[-1].strip() for linha in linhas[1:]]
            # Verificando se todas as informações necessárias estão presentes
            if all(inf[2:4]):
                return f'<p>{indice}. Jogo: {inf[0]} x {inf[1]}  Placar: {inf[2]} - {inf[3]}</p>\n'
        except Exception as e:
            print(f"Erro ao processar informações do jogo: {e}")
        return None

    def mostrar_resultados(self, dados, total_jogos):
        self.textBrowser.clear()
        self.textBrowser.append(f"Total de jogos encontrados: {total_jogos}\n")
        self.textBrowser.append('\n'.join(filter(None, dados)))

if __name__ == '__main__':
    app = QApplication([])
    janela = MeuApp()
    janela.show()
    app.exec_()
