from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from os import path

class MeuApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__(self)
        loadUi(self.localPath('interface.ui'), self)
        
    def localPath(self, relativo):
        return f'{path.dirname(path.realpath(__file__))}\\{relativo}'






if __name__ == '__main__':
    app = QApplication([])
    janela = MeuApp()
    janela.show()
    app.exec_()