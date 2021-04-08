from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QMessageBox
from qt_material import apply_stylesheet
from urllib.request import Request, urlopen
import validators
import ntpath
from bs4 import BeautifulSoup
from pln import Pln
from ventana_ui import *

app = ""


def process_text(text, directorio, titulo):
    x = Pln(text, directorio, titulo)
    x.process()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    archivos = []
    dir = ""

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.barchivo.clicked.connect(self.openFileNamesDialog)
        self.bdir.clicked.connect(self.openDir)
        self.burl.clicked.connect(self.openUrl)
        self.baceptar.clicked.connect(lambda: self.aceptar(self.archivos, self.dir))

    def openFileNamesDialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Selecciona Archivos", "", "txt Files (*.txt)")
        if files:
            for i in files:
                self.list_archivo.addItem(ntpath.basename(i))
                self.archivos.append((i, 0))

    def openDir(self):
        directorio = str(QFileDialog.getExistingDirectory(self, "Selecciona Directorio"))
        self.label_dir.setText(directorio)
        self.dir = directorio

    def openUrl(self):
        text, okPressed = QInputDialog.getText(self, "Ingrese Url", "URL:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.list_url.addItem(text)
            self.archivos.append((text, 1))

    def aceptar(self, file, ruta):
        if len(file) > 2 or ruta == "":
            QMessageBox.about(self, "Error", "No hay más de dos archivos o no se ha seleccionado directorio")
        else:
            #app.closeAllWindows()
            for i in file:
                if i[1] == 0:
                    ftemp = open(i[0], 'r', encoding="utf8", errors="ignore")
                    text = ftemp.read()
                    title = ntpath.basename(i[0]).split(".")
                    process_text(text, ruta, title[0])
                if i[1] == 1:
                    if validators.url(i[0]):
                        req = Request(i[0], headers={'User-Agent': 'Mozilla/5.0'})
                        webpage = urlopen(req).read()
                        soup = BeautifulSoup(webpage, "html.parser")
                        text = soup.get_text(strip=True)
                        title = soup.title.string
                        process_text(text, ruta, title)
                    else:
                        QMessageBox.about(self, "Error", "URL incorrecta")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    app.exec_()
