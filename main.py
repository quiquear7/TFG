import csv
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QMessageBox
from qt_material import apply_stylesheet
from urllib.request import Request, urlopen
import validators
import ntpath
import os
from bs4 import BeautifulSoup
from entrenar import EntrenarCsv
from pln import Pln
from ventana_ui import *
import fitz

app = ""


def crearcsv():
    with open('final_v6.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Title',
                             'Mu',
                             'Flesch',
                             'Por_Sinonimos',
                             'Por_Abreviaturas',
                             'Por_Siglas',
                             "Infinitive_Verbs_number",
                             "Gerund_Verbs_number",
                             "Participle_Verbs_number",
                             "Articles_number",
                             "Preposition_number",
                             "Noun",
                             "Por_Desconocidas",
                             "Por_Largas",
                             "Por_Superlativos",
                             "Por_Adverbios",
                             "Por_Simbolos",
                             "Mayusuculas_NoSiglas",
                             "Por_Inderterminados",
                             "Por_numeros",
                             "Por_complex",
                             "Por_muy_frecuentes",
                             "Por_frecuentes",
                             "Por_poco_frecuentes",
                             "Por_comillas",
                             "Por_Homo",
                             'Tipo'])


def entrenar(win, direccion):
    if dir == "":
        QMessageBox.about(win, "Error", "Seleccione ruta")
    else:
        app.closeAllWindows()
        crearcsv()

        contenido = os.listdir('GigaBDCorpus-master/Dificiles')
        for name in contenido:
            print(name)
            ruta = 'GigaBDCorpus-master/Dificiles/' + name
            ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
            text = ftemp.read()
            title = name.split(".")
            x = EntrenarCsv(text, direccion, title[0], "Dificil")
            x.process()

        '''contenido = os.listdir('GigaBDCorpus-master/Originales')
        for name in contenido:
            print(name)
            ruta = 'GigaBDCorpus-master/Originales/' + name
            doc = fitz.open(ruta)
            textPDF = ""
            for i in range(1, doc.page_count):
                page = doc.loadPage(i)
                textPDF += page.getText("text")
            title = name.split(".")
            if textPDF != "":
                x = EntrenarCsv(textPDF, direccion, title[0], "Dificil")
                x.process()
            else:
                print('vacio')

        print("Fin PDF")'''

        contenido = os.listdir('GigaBDCorpus-master/Faciles')
        for name in contenido:
            print(name)
            ruta = 'GigaBDCorpus-master/Faciles/' + name
            ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
            text = ftemp.read()
            title = name.split(".")
            x = EntrenarCsv(text, direccion, title[0], "Facil")
            x.process()

        '''contenido = os.listdir('GigaBDCorpus-master/Adaptadas')
        for name in contenido:
            print(name)
            ruta = 'GigaBDCorpus-master/Adaptadas/' + name
            doc = fitz.open(ruta)
            textPDF = ""
            for i in range(1, doc.page_count):
                page = doc.loadPage(i)
                textPDF += page.getText("text")
            title = name.split(".")
            if textPDF != "":
                x = EntrenarCsv(textPDF, direccion, title[0], "Facil")
                x.process()
            else:
                print('vacio')

        print("Fin PDF")'''


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
        self.bentrenar.clicked.connect(lambda: entrenar(self, self.dir))

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
        if len(file) < 2 or ruta == "":
            QMessageBox.about(self, "Error", "No hay más de dos archivos o no se ha seleccionado directorio")
        else:
            app.closeAllWindows()
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
