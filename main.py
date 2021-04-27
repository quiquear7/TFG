import fitz
from bson import json_util

import csv
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QMessageBox
from qt_material import apply_stylesheet
from urllib.request import Request, urlopen
import validators
import ntpath
import os
from bs4 import BeautifulSoup
from ui.analisis_ui import Ui_Analisis
from entrenar import EntrenarCsv
from pln import Pln
from ui.ventana_ui import *
import json

app = ""
fileJson = ""
nameJson = ""
resumenDoc = ""
resultados = ""


def crearcsv():
    with open('GigaBDCorpus-master/CSV/final_v12.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Title',
                             'Por_Sinonimos',
                             'Por_Abreviaturas',
                             'Por_Siglas',
                             "Por_verbs",
                             "Infinitive_Verbs_number",
                             "Gerund_Verbs_number",
                             "Participle_Verbs_number",
                             "Determiners_number",
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
                             "Ratio_Palabra_Frases",
                             "Ratio_Caracteres_Palabra",
                             "Comas",
                             "puntos",
                             "punto_y_coma",
                             "N_sentences",
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

        contenido = os.listdir('GigaBDCorpus-master/Originales')
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

        print("Fin PDF")

        contenido = os.listdir('GigaBDCorpus-master/Faciles')
        for name in contenido:
            print(name)
            ruta = 'GigaBDCorpus-master/Faciles/' + name
            ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
            text = ftemp.read()
            title = name.split(".")
            x = EntrenarCsv(text, direccion, title[0], "Facil")
            x.process()

        contenido = os.listdir('GigaBDCorpus-master/Adaptadas')
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

        print("Fin PDF")


def process_text(self, text, titulo, url):
    app.closeAllWindows()
    x = Pln(text, titulo, url)
    global resultados, fileJson, nameJson
    resultados, fileJson, nameJson = x.process()
    self.w = AnalisisWindow()
    self.w.show()
    self.hide()


class MainWindow(QtWidgets.QMainWindow, Ui_TFG):
    archivos = ""
    dir = ""

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.bdir.hide()
        # self.setWindowIcon(QtGui.QIcon('logo.png'))
        # set the title
        self.bentrenar.hide()
        self.setWindowTitle("Análisis")
        self.barchivo.clicked.connect(self.openFileNamesDialog)
        # self.bdir.clicked.connect(self.openDir)
        self.burl.clicked.connect(self.openUrl)
        self.baceptar.clicked.connect(lambda: self.aceptar(self.archivos, self.dir))
        self.btexto.clicked.connect(self.openText)
        self.bentrenar.clicked.connect(self.preEntreno)

    def preEntreno(self):
        self.pintarButton(self.bentrenar)
        self.limpiarArchivo()
        directorio = str(QFileDialog.getExistingDirectory(self, "Selección de Directorio"))
        self.dir = directorio
        self.archivos = ("", 2)
        self.listWidget.clear()
        self.listWidget.addItem(directorio)
        self.resizeLW(0)

    def openFileNamesDialog(self):
        self.pintarButton(self.barchivo)
        file, _ = QFileDialog.getOpenFileName(self, "Selección de Archivo", "", "txt File (*.txt)")
        if file:
            self.limpiarArchivo()
            self.listWidget.addItem(file)
            self.archivos = (file, 0)
            self.resizeLW(0)

    def openUrl(self):
        self.pintarButton(self.burl)
        text, okPressed = QInputDialog.getText(self, "Ingrese Url", "URL:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.limpiarArchivo()
            self.listWidget.addItem(text)
            self.archivos = (text, 1)
            self.resizeLW(0)

    def openText(self):
        self.pintarButton(self.btexto)
        text, okPressed = QInputDialog.getText(self, "Ingrese Texto", "Texto:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.limpiarArchivo()
            self.listWidget.addItem(text)
            self.archivos = (text, 3)
            self.resizeLW(1)

    def resizeLW(self, tipo):
        if tipo == 1:
            self.listWidget.resize(291, 140)
            self.baceptar.setGeometry(QtCore.QRect(240, 310, 96, 31))
        else:
            self.listWidget.resize(291, 49)
            self.baceptar.setGeometry(QtCore.QRect(240, 220, 96, 31))

    def aceptar(self, file, ruta):
        if file == "":
            QMessageBox.about(self, "Error", "No se ha seleccionado archivo")
        else:
            if file[1] == 0:
                ftemp = open(file[0], 'r', encoding="utf8", errors="ignore")
                text = ftemp.read()
                title = ntpath.basename(file[0]).split(".")
                process_text(self, text, title[0], "")
            if file[1] == 1:
                if validators.url(file[0]):
                    req = Request(file[0], headers={'User-Agent': 'Mozilla/5.0'})
                    webpage = urlopen(req).read()
                    soup = BeautifulSoup(webpage, "html.parser")
                    text = soup.get_text(strip=True)
                    title = soup.title.string
                    process_text(self, text, title, file[0])
                else:
                    QMessageBox.about(self, "Error", "URL incorrecta")
            if file[1] == 2:
                if ruta != "":
                    entrenar(self, ruta)
                else:
                    QMessageBox.about(self, "Error", "Ruta Necesaria")
            if file[1] == 3:
                tt, okPressed = QInputDialog.getText(self, "Ingrese Nombre", "Nombre:", QLineEdit.Normal, "")
                if okPressed and tt != '':
                    process_text(self, file[0], tt, "")
                else:
                    QMessageBox.about(self, "Error", "Nombre Necesario")

    def limpiarArchivo(self):
        self.archivos = ""
        self.listWidget.clear()

    def limpiarVentana(self):
        self.burl.hide()
        self.btexto.hide()
        self.barchivo.hide()
        self.bentrenar.hide()
        self.listWidget.hide()
        self.baceptar.hide()

    def pintarButton(self, button):
        qss = '''
        QPushButton{
            background-color: #31363b;
        }
        QPushButton:hover{
            background-color: #018786;
        }
        '''

        self.barchivo.setStyleSheet(qss)
        self.burl.setStyleSheet(qss)
        self.bentrenar.setStyleSheet(qss)
        self.btexto.setStyleSheet(qss)
        button.setStyleSheet('QPushButton {background-color: #232629; }')


def parse_json(data):
    return json.loads(json_util.dumps(data))


class AnalisisWindow(QtWidgets.QMainWindow, Ui_Analisis):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Resumen Análisis")
        self.bjson.clicked.connect(self.saveJson)
        self.rellenarAnalisis()

    def rellenarAnalisis(self):
        for i in resultados:
            self.listWidget.addItem(i[0] + ": " + str(i[1]))

    def saveJson(self):
        directorio = str(QFileDialog.getExistingDirectory(self, "Selección de Directorio"))
        if directorio != "":
            ajson = directorio + '/' + nameJson + '.json'

            with open(ajson, 'w', encoding='utf8') as file:
                json.dump(parse_json(fileJson), file, ensure_ascii=False, indent=4)

            if os.path.exists(ajson):
                QMessageBox.about(self, "JSON", "JSON Guardado")
            else:
                QMessageBox.about(self, "JSON Error", "JSON no se ha guardado")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    app.exec_()
