import codecs
import fitz
from PyQt5.QtGui import QTextCharFormat
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
import sys
import os
import platform
from PySide6.QtWidgets import QApplication
from modules import *
from widgets import *

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


def process_text(self, text, titulo, url):
    app.closeAllWindows()
    x = Pln(text, titulo, url)
    global resultados, fileJson, nameJson, textReturn, dic_resultados, analisis
    resultados, fileJson, nameJson, textReturn, dic_resultados, analisis = x.process()
    self.w = AnalisisWindow()
    self.w.show()
    self.hide()


class MainWindow(QtWidgets.QMainWindow, Ui_TFG):
    archivos = ""
    dir = ""

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        # self.setWindowIcon(QtGui.QIcon('logo.png'))
        # set the title
        self.setWindowTitle("Análisis")
        # self.bentrenar.hide()
        self.barchivo.clicked.connect(self.openFileNamesDialog)
        self.burl.clicked.connect(self.openUrl)
        self.baceptar.clicked.connect(lambda: self.aceptar(self.archivos, self.dir))
        self.bentrenar.clicked.connect(self.preEntreno)

    def preEntreno(self):
        self.pintarButton(self.bentrenar)
        self.limpiarArchivo()
        directorio = str(QFileDialog.getExistingDirectory(self, "Selección de Directorio"))
        self.dir = directorio
        self.archivos = ("", 2)
        self.listWidget.clear()
        self.listWidget.addItem(directorio)

    def openFileNamesDialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selección de Archivo", "", "txt File (*.txt);;PDF Files (*.pdf)")
        if file:
            self.pintarButton(self.barchivo)
            self.limpiarArchivo()
            self.listWidget.addItem(file)
            self.archivos = (file, 0)

    def openUrl(self):
        text, okPressed = QInputDialog.getText(self, "Ingrese Url", "URL:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.pintarButton(self.burl)
            self.limpiarArchivo()
            self.listWidget.addItem(text)
            self.archivos = (text, 1)

    def aceptar(self, file, ruta):
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
                    process_text(self, text, title[0], "")
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
                        process_text(self, text, title, file[0])
                else:
                    QMessageBox.about(self, "Error", "URL incorrecta")
            if file[1] == 2:
                if ruta != "":
                    entrenar(self, ruta)
                else:
                    QMessageBox.about(self, "Error", "Ruta Necesaria")

    def limpiarArchivo(self):
        self.archivos = ""
        self.listWidget.clear()

    def limpiarVentana(self):
        self.burl.hide()
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
        button.setStyleSheet('QPushButton {background-color: #232629; }')


def parse_json(data):
    return json.loads(json_util.dumps(data))


class AnalisisWindow(QtWidgets.QMainWindow, Ui_Analisis):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Resumen Análisis")
        self.bjson.clicked.connect(self.saveJson)
        self.banalisis.clicked.connect(lambda: inicio(self))
        self.rellenarAnalisis()

    def rellenarAnalisis(self):

        for i in resultados:
            item = i[0] + ": " + str(i[1])[0:7]
            self.listWidget.addItem(item)

        nums = {}
        for i in dic_resultados:
            if len(dic_resultados[i]) > 0:
                for j in dic_resultados[i]:
                    nums[j[1]] = i
        cont = 0
        html = ""
        text = ""

        for i in analisis:
            if cont in nums:

                text += "<font color="'red'" title=" + nums[cont] + ">" + i[0] + " " + "</font>"
                # html += "<p style="'color:#FF0000'" title=" + nums[cont] + ">" + i[0] + "</p>"
            else:
                text += i[0] + " "
            cont += 1
        print(text)
        self.textBrowser.setHtml(text)

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


def inicio(self):
    app.closeAllWindows()
    apply_stylesheet(app, theme='dark_teal.xml')
    self.w = MainWindow()
    self.w.show()
    self.hide()


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

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)


        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_dark.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        widgets.plainTextEdit.hide()
        widgets.textBrowser.setText("hola")
        widgets.barchivo.clicked.connect(lambda: self.openFileNamesDialog(widgets))
        widgets.urlb.clicked.connect(lambda: self.openUrl(widgets))
        widgets.pushButton_3.clicked.connect(lambda: self.aceptar(self.archivos, self.dir, widgets))
        widgets.btextPlano.clicked.connect(lambda: self.textPlano(widgets))

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
            #self.pintarButton(self.barchivo)
            self.limpiarArchivo(widgets)
            widgets.textBrowser.setText(file)
            self.archivos = (file, 0)

    def openUrl(self, widgets):
        self.hideT(widgets)
        text, okPressed = QInputDialog.getText(self, "Ingrese Url", "URL:", QLineEdit.Normal, "")
        if okPressed and text != '':
            #self.pintarButton(self.burl)
            self.limpiarArchivo(widgets)
            widgets.textBrowser.setText(text)
            self.archivos = (text, 1)

    def aceptar(self, file, ruta, widgets):
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
                    process_text(self, text, title[0], "")
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
                        process_text(self, text, title, file[0])
                else:
                    QMessageBox.about(self, "Error", "URL incorrecta")
            if file[1] == 2:
                if ruta != "":
                    entrenar(self, ruta)
                else:
                    QMessageBox.about(self, "Error", "Ruta Necesaria")
            if file[1] == 3:
                text = widgets.plainTextEdit.toPlainText()
                print(text)
                if len(text) == 0:
                    QMessageBox.about(self, "Error", "Texto Necesari0")

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

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Analizador Textos")
    app.setWindowIcon(QIcon("logo.svg"))
    window = MainWindow()
    sys.exit(app.exec())

    '''app = QtWidgets.QApplication([])
    window = MainWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    app.exec_()'''
