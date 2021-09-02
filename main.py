import codecs
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
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
from entrenar import EntrenarCsv
from pln import Pln
import json
import sys
import os
import platform
from PySide6.QtWidgets import QApplication
from modules import *
from widgets import *
import threading
import pln

os.environ["QT_FONT_DPI"] = "96"
widgets = None

app = ""
fileJson = ""
nameJson = ""

"""Crea el archivo CSV, con los encabezados de las variables, en el directorio indicado. Este archivo es editado poste-
riormente, agregando los valores de las variables de cada documento, en la fase de entrenamiento"""
def crearcsv(directory):
    with open(directory + '/entrenamiento.csv', 'w', newline='') as csvfile:
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
                             "nombres_propios",
                             "nombres_propios/noun",
                             "futuro",
                             "futuro/verbs",
                             "pasado",
                             "pasado/verbs",
                             'Tipo'])

"""función que nos permite parsear el json para que pueda ser guardado"""
def parse_json(data):
    return json.loads(json_util.dumps(data))


"""clase para crear la ventana"""
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
        description = "Analizador de Textos"

        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        UIFunctions.uiDefinitions(self)
        self.thread = {}
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)

        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        self.show()

        widgets.stackedWidget.setCurrentWidget(widgets.home)

        """botón de home"""
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        widgets.plainTextEdit.hide() # oculta el cuadro de texto

        """botón para seleccionar un archivo"""
        widgets.barchivo.clicked.connect(self.openFileNamesDialog)

        """botón para ingresar una URL"""
        widgets.urlb.clicked.connect(self.openUrl)

        """botón para comenzar el análisis del texto"""
        widgets.pushButton_3.clicked.connect(lambda: self.aceptar(self.archivos, self.dir))

        """botón para mostrar el cuadro de texto plano"""
        widgets.btextPlano.clicked.connect(self.textPlano)

        """botón para guardar el json en el equipo"""
        widgets.bjson.clicked.connect(self.saveJson)

        """establecemos el diseño"""
        widgets.listAnalisis.setStyleSheet("*{border: 2px solid rgb(91, 101, 124);"
                                           "border-radius: 5px;"
                                           "padding: 10px}")

        """botón para comenzar el entrenamiento"""
        widgets.bAceptar.clicked.connect(self.entrenar)

        """"ocultamos ls barra de progreso"""
        widgets.progressBar.hide()

        self.analisisHide()

    """función para mostrar los resultados del análisis"""
    def analisisShow(self):
        widgets.progressBar.hide()  # ocultamos barra de progreso
        widgets.listAnalisis.show()  # list view con información del analisis
        widgets.textAnalisis.show()  # list view con el texto del análisis
        widgets.tituloAnalisis.show()  # titulo del analisis
        widgets.bjson.show()  # botón para guardar json

    """función para ocultar los resultados del análisis"""
    def analisisHide(self):
        widgets.listAnalisis.hide()
        widgets.textAnalisis.hide()
        widgets.tituloAnalisis.hide()
        widgets.bjson.hide()

    """función para mostrar el cuadro de texto plano"""
    def hideT(self):
        widgets.plainTextEdit.hide()

    """función para ocultar el cuadro de texto plano"""
    def showT(self):
        widgets.plainTextEdit.show()
        widgets.textBrowser.clear()

    """función para indicar que se va a utilizar texto plano como método de entrada"""
    def textPlano(self):
        self.showT()  # mostramos el cuadro de texto
        self.archivos = ("", 3)  # indicamos el tipo de entrada que se va a utilizar

    """función para seleccionar un archivo para analizar"""
    def openFileNamesDialog(self):
        self.hideT()
        file, _ = QFileDialog.getOpenFileName(self, "Selección de Archivo", "", "txt File (*.txt);;PDF Files (*.pdf)")  # obtenemos el archivo
        if file:
            self.limpiarArchivo()
            widgets.textBrowser.addItem("Archivo Seleccionado: " + file)  # mostramos por pantalla el nombre del archivo
            self.archivos = (file, 0)  # indicamos el metodo que se ha utilizado para obtener el texto

    """función para seleccionar una URL para analizar"""
    def openUrl(self):
        self.hideT()

        """establecemos el diseño del cuadro de dialogo"""
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setStyleSheet(u"background-color: rgb(27, 29, 35);"
                          u"color:#FFFFFF;"
                          u"font-size:17px;")
        dlg.setLabelText("URL:")
        dlg.resize(500, 100)
        ok = dlg.exec()
        url = dlg.textValue()  # obtenemos el texto

        if ok and url != '':
            self.limpiarArchivo()
            widgets.textBrowser.addItem("URL: " + url)  # mostramos url
            self.archivos = (url, 1) # indicamos el metodo que se ha utilizado para obtener el texto

    """función para relizar el proceso de entrenamiento"""
    def entrenar(self):
        directorio = str(QFileDialog.getExistingDirectory(self, "Selección de Directorio"))  # ruta donde se guarda el csv
        if directorio == "":
            msg = QMessageBox(self)
            msg.about(self, "Error", "Seleccione ruta")
        else:
            self.close()
            crearcsv(directorio)
            cont = 1

            """recorremos las rutas donde están los archivos a analizar"""
            contenido = os.listdir('GigaBDCorpus-master/Dificiles')
            for name in contenido:
                print(cont, name)
                ruta = 'GigaBDCorpus-master/Dificiles/' + name
                ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
                text = ftemp.read() # obtenemos texto del archivo
                title = name.split(".")  # obtenenmos título del archivo
                x = EntrenarCsv(text, directorio, title[0], "Dificil")
                x.process()  # relizamos la extracción de variables
                cont += 1

            contenido = os.listdir('GigaBDCorpus-master/Faciles')
            for name in contenido:
                print(cont, name)
                ruta = 'GigaBDCorpus-master/Faciles/' + name
                ftemp = open(ruta, 'r', encoding="utf-8-sig", errors="ignore")
                text = ftemp.read()
                title = name.split(".")
                x = EntrenarCsv(text, directorio, title[0], "Facil")
                x.process()
                cont += 1

    """función que obtiene el texto de la entrada seleccionada para realizar el analisis"""
    def aceptar(self, file, ruta):
        self.analisisHide()

        """mostramos un mensaje si no se ha ingresado ningún texto"""
        if file == "":
            msg = QMessageBox(self)
            msg.setStyleSheet(u"background-color: rgb(27, 29, 35);"
                              u"color:#FFFFFF;"
                              u"font-size:17px;")
            msg.about(self, "Error", "No se ha detectado ningún metodo de entrada")
        else:

            """Archivo"""
            if file[1] == 0:
                extension = file[0].split(".") # comprobamos extensión del archivo
                text = ""

                """extensión del archivo es txt"""
                if extension[1] == "txt":
                    ftemp = open(file[0], 'r', encoding="utf8", errors="ignore")
                    text = ftemp.read() # obtenemos texto del archivo

                """extensión del archivo es pdf"""
                if extension[1] == "pdf":
                    doc = fitz.open(file[0])
                    for i in range(1, doc.page_count):
                        page = doc.loadPage(i)
                        text += page.getText("text")  # obtenemos texto del archivo

                """comprobamos que el archivo se ha leido bien"""
                if len(text) == 0:
                    msg = QMessageBox(self)
                    msg.setStyleSheet(u"background-color: rgb(27, 29, 35);"
                                      u"color:#FFFFFF;"
                                      u"font-size:17px;")
                    msg.about(self, "Error", "No se puede obtener texto")
                else:
                    title = ntpath.basename(file[0]).split(".")  # obtenemos titulo del archivo
                    self.process_text(text, title[0], "")  # comenzamos el analisis del texto
            """URL"""
            if file[1] == 1:
                """ validamos la url"""
                if validators.url(file[0]):
                    req = Request(file[0], headers={'User-Agent': 'Mozilla/5.0'})
                    webpage = urlopen(req).read()
                    soup = BeautifulSoup(webpage, "html.parser")
                    text = soup.get_text(strip=True)  # obtenemos texto de la página web
                    """comprobamos que el texto se ha leido bien"""
                    if len(text) == 0:
                        msg = QMessageBox(self)
                        msg.setStyleSheet(u"background-color: rgb(27, 29, 35);"
                                          u"color:#FFFFFF;"
                                          u"font-size:17px;")
                        msg.about(self, "Error", "No se puede obtener texto")
                    else:
                        title = soup.title.string  # obtenemos titulo de la web
                        self.process_text(text, title[0], file[0])  # comenzamos el analisis del texto
                else:

                    QMessageBox.about(self, "Error", "URL incorrecta")

            """texto plano"""
            if file[1] == 3:
                text = widgets.plainTextEdit.toPlainText()  # obtiene texto del cuadro de texto

                """cuadro para solicitar al usuario que ingrese un titulo"""
                dlg = QInputDialog(self)
                dlg.setInputMode(QInputDialog.TextInput)
                dlg.setStyleSheet("*{background-color: rgb(27, 29, 35);"
                                  "color:#FFFFFF;}")

                dlg.setLabelText("Titulo:")
                dlg.resize(300, 100)
                ok = dlg.exec()
                title = dlg.textValue()  # obtenemos el titulo ingresado

                """comprobamos que sea válido y si no mostramos un error """
                if ok and title != '':
                    if len(text) == 0:
                        QMessageBox.about(self, "Error", "Texto Necesario")
                    else:
                        self.process_text(text, title, "") # llamamos a la función para ejecutar el analisis
                else:
                    QMessageBox.about(self, "Error", "Titulo Necesario")

    """limpiar el campo que indica el archivo que se ha seleccionado"""
    def limpiarArchivo(self):
        self.archivos = ""
        widgets.textBrowser.clear()



    """funcion para realizar el analisis, utiliza hilos para que no se bloquee la interfaz"""
    def process_text(self, text, titulo, url):
        widgets.progressBar.setValue(0) # establecemos el valor inicial de la barra en 0
        self.thread = Pln(text, titulo, url, None)
        self.thread.started2.connect(self.pintarBarra)  # señal que envia el porcentaje del analisis a la funcion indicada
        self.thread.final_signal.connect(self.analisis)  # señal que se envia al finalizar el analisis
        self.thread.start()  # ejecutamos el hilo que realiza el analisis
        widgets.stackedWidget.setCurrentWidget(widgets.widgets)  # SET PAGE
        UIFunctions.resetStyle(self, 'btn_widgets')  # RESET ANOTHERS BUTTONS SELECTED
        widgets.btn_widgets.setStyleSheet(UIFunctions.selectMenu(widgets.btn_widgets.styleSheet()))
        widgets.progressBar.show()

    """función que cambiar el valor de progreso de la barra de analisis"""
    def pintarBarra(self, counter):
        widgets.progressBar.setValue(counter)

    """funcion que muestra la información del analisis"""
    def analisis(self, dic_resultados1, dic_resultados2):
        self.analisisShow()
        self.rellenarAnalisis(dic_resultados1, dic_resultados2)

    """función que guarda el json en la ruta seleccionada"""
    def saveJson(self):
        directorio = str(QFileDialog.getExistingDirectory(self, "Selección de Directorio"))  # obtenemos el directorio
        if directorio != "":
            ajson = directorio + '/' + nameJson + '.json'

            """guardamos el archivo"""
            with open(ajson, 'w', encoding='utf8') as file:
                json.dump(parse_json(fileJson), file, ensure_ascii=False, indent=4)

            """comprobamos que se ha guardado correctamente"""
            if os.path.exists(ajson):
                QMessageBox.about(self, "JSON", "JSON Guardado")
            else:
                QMessageBox.about(self, "JSON Error", "JSON no se ha guardado")

    """funcion que recibe los resultados del analisis y los muestra por pantalla"""
    def rellenarAnalisis(self, dic_resultados, dic_resultados2):
        resultados = dic_resultados2['resultados']
        titleA = dic_resultados2['titulo']  # obtenemos titulo del documento
        textReturn = dic_resultados2['texto']  # obtenemos texto

        global fileJson, nameJson
        fileJson = dic_resultados2['json']  # obtenemos json
        nameJson = dic_resultados2['titulo']  # obtenemos nombre del json

        dic_explicaciones = {}
        sigl = codecs.open("diccionarios/variables.txt", "r", encoding="utf-8")
        for entrada in sigl:
            pal = entrada.split(":")
            dic_explicaciones[pal[0]] = pal[1]
        resumen = resultados[0][1]

        if resumen == "Dificil":
            textA = "Título: " + titleA + "<br/><br/>"  # escribimos titulo del documento
            for i in resultados:
                """escribimos los resultadoso de las variables"""
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

            """escribimos el texto marcando en rojo los errores"""
            for j in frases:
                words = word_tokenize(j, "spanish")
                for i in words:
                    if i in palabras:
                        text += "<font color="'red'" title=" + palabras2[i] + ">" + i + " " + "</font>"
                    else:
                        text += i + " "
                text += "<br/>"

            widgets.textAnalisis.setHtml(text)
        else:
            textA = "Título: " + titleA + "\n\n"
            textA += "Resumen: Fácil\n\nEl texto se ha identificado como fácil no es necesario realizar ningún cambio"
            widgets.listAnalisis.setText(textA)
            widgets.textAnalisis.setText(textReturn)

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

        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Analizador Textos")
    app.setWindowIcon(QIcon("logo.svg"))
    window = MainWindow()
    sys.exit(app.exec())
