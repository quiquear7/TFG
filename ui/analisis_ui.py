# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Analisis(object):
    def setupUi(self, Analisis):
        Analisis.setObjectName("Analisis")
        Analisis.setFixedSize(800, 600)
        Analisis.setStyleSheet("/*Cambiamos el color de la ventana*/\n"
"    QMainWindow{\n"
"        background-color: #FFFFFF;\n"
"    }\n"
"\n"
"    /*Estilos para el botón*/\n"
"    QPushButton{\n"
"        background-color: #4db6ac;\n"
"        border-radius: 4px;\n"
"        color: #fff;\n"
"        font-family: \'Roboto\';\n"
"        font-size: 15px;\n"
"    }\n"
"    \n"
"    /*Definimos el estilo para un efecto hover sobre el botón,\n"
"    este cambiará su background cuando pasemos el mouse por\n"
"    encima*/\n"
"    QPushButton:hover{\n"
"    background-color: #018786;\n"
"    }\n"
"\n"
"    /*Definimos los estilos para los QLineEdit*/\n"
"    QLineEdit{\n"
"        border-radius: 3px;\n"
"        border: 2px solid #00796b;\n"
"    }\n"
"\n"
"\n"
"    \n"
"    /*Definimos el estilo para un efecto hover sobre el botón,\n"
"    este cambiará su background cuando pasemos el mouse por\n"
"    encima*/\n"
"    \n"
"\n"
"    /*Definimos los estilos para los QLabel*/\n"
"    QLabel{\n"
"        font-family: \'Roboto\';\n"
"    }\n"
"\n"
"    /*Definimos los estilos para los QLabels cuyos nombres son\n"
"    \'label_usuario\' y \'label-password\'*/\n"
"    #label_usuario, #label_password{\n"
"        font-size: 17px;\n"
"        color: #212121;\n"
"    }\n"
"    \n"
"    /*Estilo para el QLable cuyo nombre es #label_login*/\n"
"    #label_titulo{\n"
"        font-size:15px;\n"
"        color: #000000;\n"
"    }")
        self.centralwidget = QtWidgets.QWidget(Analisis)
        self.centralwidget.setObjectName("centralwidget")
        self.titulo = QtWidgets.QLabel(self.centralwidget)
        self.titulo.setGeometry(QtCore.QRect(350, 10, 150, 20))
        self.titulo.setObjectName("titulo")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 771, 471))
        self.listWidget.setObjectName("listWidget")
        self.bjson = QtWidgets.QPushButton(self.centralwidget)
        self.bjson.setGeometry(QtCore.QRect(320, 520, 75, 23))
        self.bjson.setObjectName("bjson")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 40, 771, 471))
        self.textBrowser.setObjectName("textBrowser")
        self.banalisis = QtWidgets.QPushButton(self.centralwidget)
        self.banalisis.setGeometry(QtCore.QRect(400, 520, 75, 23))
        self.banalisis.setObjectName("banalisis")
        Analisis.setCentralWidget(self.centralwidget)

        self.retranslateUi(Analisis)
        QtCore.QMetaObject.connectSlotsByName(Analisis)

    def retranslateUi(self, Analisis):
        _translate = QtCore.QCoreApplication.translate
        Analisis.setWindowTitle(_translate("Analisis", "MainWindow"))
        self.titulo.setText(_translate("Analisis", "Resumen Análisis"))
        self.bjson.setText(_translate("Analisis", "JSON"))
        self.banalisis.setText(_translate("Analisis", "Inicio"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Analisis = QtWidgets.QMainWindow()
    ui = Ui_Analisis()
    ui.setupUi(Analisis)
    Analisis.show()
    sys.exit(app.exec_())
