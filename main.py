import codecs
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import fitz
from PyQt5.QtGui import QTextCharFormat
from bson import json_util
from nltk import word_tokenize, sent_tokenize

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
import sys
import os
import platform
from PySide6.QtWidgets import QApplication
from modules import *
from widgets import *
import threading

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%
widgets = None

app = ""
fileJson = ""
nameJson = ""
resumenDoc = ""
resultados = ""
textReturn = ""
dic_resultados = {}
analisis = []


def crearcsv(directory):
    with open(directory + '/final_v57.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Title',
                             'Por_Sinonimos',
                             'Por_Abreviaturas',
                             'Por_Siglas',
                             "Por_verbs",
                             "Infinitive_Verbs_number",
                             "Gerund_Verbs_number",
                             "Participle_Verbs_number",
                             "imperative_Verbs_number",
                             "Determiners_number",
                             "Preposition_number",
                             "Noun",
                             "Por_Largas",
                             "Por_Superlativos",
                             "Por_Adverbios_mente",
                             "Por_Adverbios",
                             "Por_Simbolos",
                             "Por_Inderterminados",
                             "Por_numeros",
                             "Por_complex",
                             "Por_muy_frecuentes",
                             "Por_frecuentes",
                             "Por_poco_frecuentes",
                             "Por_muy_frecuentes_sub",
                             "Por_frecuentes_sub",
                             "Por_poco_frecuentes_sub",
                             "Por_comillas",
                             "Por_Homo",
                             "Ratio_Palabra_Frases",
                             "Ratio_Caracteres_Palabra",
                             "Comas/frases",
                             "%comas",
                             "%puntos",
                             "punto_y_coma",
                             "date",
                             "%date_mal",
                             "doble_negacion",
                             "partitivos o porcentajes",
                             "presente_indicativo",
                             "presente_indicativo/verbs",
                             "subjuntivo",
                             "condicional",
                             "nverbseguidos",
                             "%puntuacion",
                             "%etc",
                             "%mayus_no_sigla",
                             "%sin_palabras",
                             "%ordinales",
                             "%romanos",
                             "%general",
                             "%especifico",
                             "%dos_puntos",
                             "%otro_idioma",
                             "#words",
                             "#frases",
                             'Tipo'])


def entrenar(win, direccion):
    long_media = 0
    if dir == "":
        QMessageBox.about(win, "Error", "Seleccione ruta")
    else:
        app.closeAllWindows()
        crearcsv(direccion)
        cont = 1

        contenido = os.listdir('GigaBDCorpus-master/Dificiles')
        for name in contenido:
            print(cont, name)
            ruta = 'GigaBDCorpus-master/Dificiles/' + name
            ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
            text = ftemp.read()
            long_media += len(text)
            title = name.split(".")
            x = EntrenarCsv(text, direccion, title[0], "Dificil")
            x.process()
            cont += 1

        contenido = os.listdir('GigaBDCorpus-master/Faciles')
        for name in contenido:
            print(cont, name)
            ruta = 'GigaBDCorpus-master/Faciles/' + name
            ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
            text = ftemp.read()
            long_media += len(text)
            title = name.split(".")
            x = EntrenarCsv(text, direccion, title[0], "Facil")
            x.process()
            cont += 1


def parse_json(data):
    return json.loads(json_util.dumps(data))


class MainWindow(QMainWindow):
    archivos = ""
    dir = ""

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "Analizador de Textos"
        description = "TFG - Enrique de Aramburu"

        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)

        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)

        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        self.show()

        useCustomTheme = False
        themeFile = "themes/py_dracula_light.qss"

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        widgets.plainTextEdit.hide()
        widgets.textBrowser.setText("")
        widgets.barchivo.clicked.connect(lambda: self.openFileNamesDialog(widgets))
        widgets.urlb.clicked.connect(lambda: self.openUrl(widgets))
        widgets.pushButton_3.clicked.connect(lambda: self.aceptar(self.archivos, self.dir, widgets))
        widgets.btextPlano.clicked.connect(lambda: self.textPlano(widgets))
        widgets.bjson.clicked.connect(self.saveJson)


        self.analisisHide()

    def analisisShow(self):
        widgets.listAnalisis.show()
        widgets.textAnalisis.show()
        widgets.tituloAnalisis.show()
        widgets.bjson.show()

    def analisisHide(self):
        widgets.listAnalisis.hide()
        widgets.textAnalisis.hide()
        widgets.tituloAnalisis.hide()
        widgets.bjson.hide()

    def hideT(self, widgets):
        widgets.plainTextEdit.hide()

    def showT(self, widgets):
        widgets.plainTextEdit.show()
        widgets.textBrowser.setText("")

    def textPlano(self, widgets):
        self.showT(widgets)
        self.archivos = ("", 3)

    def openFileNamesDialog(self, widgets):
        self.hideT(widgets)
        file, _ = QFileDialog.getOpenFileName(self, "Selección de Archivo", "", "txt File (*.txt);;PDF Files (*.pdf)")
        if file:
            self.limpiarArchivo(widgets)
            widgets.textBrowser.setText("Archivo Seleccionado: " + file)
            self.archivos = (file, 0)

    def openUrl(self, widgets):
        self.hideT(widgets)
        text, okPressed = QInputDialog.getText(self, "Ingrese Url", "URL:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.limpiarArchivo(widgets)
            widgets.textBrowser.setText("URL: " + text)
            self.archivos = (text, 1)

    def aceptar(self, file, ruta, widgets):
        self.analisisHide()

        if file == "":
            QMessageBox.about(self, "Error", "No se ha seleccionado archivo o URL")
        else:
            if file[1] == 0:
                extension = file[0].split(".")
                text = ""
                if extension[1] == "txt":
                    ftemp = open(file[0], 'r', encoding="utf8", errors="ignore")
                    text = ftemp.read()
                if extension[1] == "pdf":
                    doc = fitz.open(file[0])
                    for i in range(1, doc.page_count):
                        page = doc.loadPage(i)
                        text += page.getText("text")
                if len(text) == 0:
                    QMessageBox.about(self, "Error", "No se puede obtener texto")
                else:
                    title = ntpath.basename(file[0]).split(".")
                    QMessageBox.about(self, "Info", "Realizando Análisis")
                    self.process_text(text, title[0], "")
                    '''hilo1 = threading.Thread(target=self.process_text, args=(text, title[0], "",), daemon=True)
                    hilo1.start()'''
            if file[1] == 1:
                if validators.url(file[0]):
                    req = Request(file[0], headers={'User-Agent': 'Mozilla/5.0'})
                    webpage = urlopen(req).read()
                    soup = BeautifulSoup(webpage, "html.parser")
                    text = soup.get_text(strip=True)
                    if len(text) == 0:
                        QMessageBox.about(self, "Error", "No se puede obtener texto")
                    else:
                        title = soup.title.string
                        QMessageBox.about(self, "Info", "Realizando Análisis")
                        '''hilo1 = threading.Thread(target=self.process_text, args=(text, title[0], file[0],), daemon=True)
                        hilo1.start()'''

                else:
                    QMessageBox.about(self, "Error", "URL incorrecta")
            if file[1] == 2:
                if ruta != "":
                    entrenar(self, ruta)
                else:
                    QMessageBox.about(self, "Error", "Ruta Necesaria")
            if file[1] == 3:
                text = widgets.plainTextEdit.toPlainText()
                title, okPressed = QInputDialog.getText(self, "Ingrese Titulo", "Titulo:", QLineEdit.Normal, "")
                if okPressed and title != '':
                    if len(text) == 0:
                        QMessageBox.about(self, "Error", "Texto Necesari0")
                    else:
                        QMessageBox.about(self, "Info", "Realizando Análisis")
                        hilo1 = threading.Thread(target=self.process_text, args=(text, title, "",), daemon=True)
                        hilo1.start()
                else:
                    QMessageBox.about(self, "Error", "Titulo Necesari0")

    def limpiarArchivo(self, widgets):
        self.archivos = ""
        widgets.textBrowser.setText("")

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

    def process_text(self, text, titulo, url):
        x = Pln(text, titulo, url)
        global resultados, fileJson, nameJson, textReturn, dic_resultados, analisis
        resultados, fileJson, nameJson, textReturn, dic_resultados, analisis = x.process()
        self.analisis(resultados, analisis)

    def analisis(self, resultados, analisis):
        self.analisisShow()
        widgets.stackedWidget.setCurrentWidget(widgets.widgets)  # SET PAGE
        UIFunctions.resetStyle(self, 'btn_widgets')  # RESET ANOTHERS BUTTONS SELECTED
        widgets.btn_widgets.setStyleSheet(UIFunctions.selectMenu(widgets.btn_widgets.styleSheet()))
        self.rellenarAnalisis(resultados, analisis)

    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)

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

    def rellenarAnalisis(self, resultados, analisis):
        dic_explicaciones = {}
        sigl = codecs.open("diccionarios/variables.txt", "r", encoding="utf-8")
        for entrada in sigl:
            pal = entrada.split(":")
            dic_explicaciones[pal[0]] = pal[1]

        textA = ""
        for i in resultados:
            textA += i[0] + ": " + str(i[1])[0:7]
            textA += "<br/>"
            if i[0] != 'Resumen':
                textA += dic_explicaciones[i[0]]
                textA += "<br/>"
                textA += "<br/>"

        widgets.listAnalisis.setHtml(textA)

        palabras = {}
        palabras2 = {}
        for i in dic_resultados:
            if len(dic_resultados[i]) > 0:
                for j in dic_resultados[i]:
                    palabras2[j[0]] = i
                    if j[0] not in palabras:
                        palabras[j[0]] = dic_explicaciones[i]
                    else:
                        palabras[j[0]] += dic_explicaciones[i]

        text = ""
        frases = textReturn.split("\n")

        for j in frases:
            words = word_tokenize(j, "spanish")
            for i in words:
                if i in palabras:
                    text += "<font color="'red'" title=" + palabras2[i] + ">" + i + " " + "</font>"
                    print(palabras[i])
                else:
                    text += i + " "
            text += "<br/>"

        widgets.textAnalisis.setHtml(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Analizador Textos")
    app.setWindowIcon(QIcon("logo.svg"))
    window = MainWindow()
    sys.exit(app.exec())
