# TFG
Proyecto TFG 2021 de Enrique de Aramburu.

Analizador de Textos. Es necesaria una instalación de FreeLing.

# Instalación

(Se ha utilizado Ubuntu)

1. Instalar Python 3.8
2. Instalar FreeLing siguiendo los pasos del siguiente enlace https://freeling-user-manual.readthedocs.io/en/v4.2/

Instalar Módulos

3. pip install pyqt5
4. pip install pymupdf
5. pip install pymongo
6. pip install nltk
7. pip install qt-material
8. pip install validators
9. pip install beautifulsoup4
10. pip install pyenchant
11. pip install PySide6
12. pip install legibilidad
13. pip install textstat

#Funcionamiento

El programa tiene dos funciones:
1. Extractor de Características: se usa en la fase de entrenamiento, la ruta de la que se obtienen los textos ya está
previamente definida. La extración se guarda en un archivo csv. Para iniciarla hay que abrir el programa y seleccionar
la opción entrenamiento, se abrirá un cuadro para seleccionar la ruta donde se guardará el archivo y se iniciará el
proceso en segundo plano. 
2. Analizador de Textos: seleccionar un archivo desde el programa y pulsar el botón de comenzar. 
