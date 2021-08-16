import codecs
import math
import pickle
import string
from time import time
import enchant
import nltk
import nltk.data
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PySide6.QtCore import QThread, QObject, Signal
import dic as dic
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from legibilidad import legibilidad
import textstat


class Pln(QThread):
    """señal para enviar el porcentaje de análisis realizado"""
    started2 = Signal(int)

    '''señal para enviar los resultados del analisis en diccionarios'''
    final_signal = Signal(dict, dict)

    def __init__(self, text, title, url, parent=None):
        QThread.__init__(self, parent)
        self.is_running = True
        self.text = text  # texto que se va a analizar
        self.title = title  # titulo del documento
        self.url = url  # url del documento (en caso de que sea una url)

    def run(self):
        """obtenemos el nombre del archivo eliminando espacios y signos de puntación"""
        punct = string.punctuation
        self.title = self.title.replace(" ", "")
        for c in punct:
            self.title = self.title.replace(c, "")

        '''Rellenamos json'''
        fjson = {
            "Title": self.title,
            "URL": self.url,
            "Format": "csv",
            "Topic": "",
            "Aimed_to": "",
            "Character": "",
            'Readability_Set': {
                'mu_Index': legibilidad.mu(self.text),
                'Flesch-kincaid_index': textstat.flesch_kincaid_grade(self.text)
            }
        }

        '''obtenemos una lista con el texto dividido en frases '''
        frases = sent_tokenize(self.text, "spanish")

        '''obtenemos una lista con palabras '''
        words = word_tokenize(self.text, "spanish")

        '''obtenemos una lista de tuplas con las frecuencias de las palabras'''
        freq = nltk.FreqDist(words)

        punct = string.punctuation  # lista con los signos de puntación

        '''creamos una lista de tuplas con la palabra y su frecuencia'''
        freq2 = []
        for i in freq:
            if i not in punct:
                freq2.append((i, freq[i]))

        '''calculamos los caracteres totales de las palabras'''
        caracteres = 0
        for i in words:
            caracteres += len(i)

        self.started2.emit(10)  # envimaos porcentaje de analisis, para mostrarlo en la barra

        '''obtenemos los diccionarios que vamos a utilizar en el texto'''

        dic_frecuencia = dic.diccionario_frecuencia()
        self.started2.emit(11)

        dic_frecuencia_sub = dic.diccionario_frecuencia_sub()

        self.started2.emit(15)

        '''analisis nos devuelve una lista con el etiquetado de las palabras, en lenwords se alamacena el número de 
        palabras etiquetadas'''
        analisis, lenwords = dic.freeling(self.text, self.started2)
        if lenwords == 0:
            entrada = open('diccionarios/etiquetador-spa.pkl', 'rb')
            etiquetador = pickle.load(entrada)
            analisis = etiquetador.tag(words)
            lenwords = len(words)
            entrada.close()

        cont = 0  # indica la posición en la que se encuentra la palabra

        large = []  # almacena las palabras largas
        comillas = []  # almacena las comillas
        presente_indicativo = []  # almacena verbos en presente de indicativo
        determiner = []  # almacena determinantes en el texto
        noun = []  # almacena los sustantivos del texto
        preposition = []  # almacena las preposiciones del texto
        verbs = []  # almacena los verbos del texto
        verbi = []  # almacena los verbos en infinitivo
        verbg = []  # almacena los verbos en gerundio del texto
        verbp = []  # almacena los participios del texto
        number = []  # almacena los numeros en el texto
        date = []  # alamcena las fechas del texto
        desconocidas = []  # almacena las palabras desconocidas
        comas = []  # almacena las comas del texto
        muy_frecuentes_sub = []  # almacena las palabras muy frecuentes del texto usando el listado de subtitulos
        frecuentes_sub = []  # almacena las palabras frecuentes en el texto usando el listado de subtitulos
        poco_frecuentes_sub = []  # almacena las palabras poco frecuentes en el texto usando el listado de subtitulos
        verbos_no_indicativo = []  # alamacena los verbos que no están en indicativo
        proper_noun = []  # almacena sutantivos propios

        '''en este momento recorremos una a una cada palabra etiquetada'''
        for x in analisis:
            i = x[0]  # palabra a analizar
            j = x[1]  # etiqueta

            '''si la palabra tiene mas de 10 caracteres es considerada larga '''
            if len(i) > 10 and "_" not in i:
                large.append((i, cont))

            '''si la palabra es igual a alguna de las siguientes es considerada comilla '''
            if '"' == i or "«" == i or "»" == i or "'" == i:
                comillas.append((i, cont))

            '''determinantes'''
            if j[0] == "D":
                determiner.append((i, cont))

            '''Sustantivos'''
            if j[0] == "N":
                noun.append((i, cont))

                '''sutantivo propio'''
                if j[1] == "P":
                    proper_noun.append(i)

            '''vebos'''
            if j[0] == "V":
                verbs.append((i, cont))

                '''verbos en infinitivo'''
                if j[2] == "N":
                    verbi.append((i, cont))

                '''verbos en gerundio'''
                if j[2] == "G":
                    verbg.append((i, cont))

                '''verb os en participio'''
                if j[2] == "P":
                    verbp.append((i, cont))

                '''verbos en presente indicativo'''
                if j[2] == "I" and j[3] == "P":
                    presente_indicativo.append((i, cont))

                '''verbos que no esten en indicativo'''
                if j[2] != "I":
                    verbos_no_indicativo.append((i, cont))

            '''numeros'''
            if j[0] == "Z":
                number.append(i)

            '''fechas'''
            if j == "W":
                date.append((i, cont))

            '''preposiciones'''
            if j == "SP":
                preposition.append((i, cont))

            '''comas'''
            if j == "Fc":
                comas.append((j, cont))

            '''calculamos las frecuencias de las palabras'''
            if i.lower() in dic_frecuencia_sub:

                '''muy frecuentes'''
                if dic_frecuencia_sub[i.lower()] >= 108:
                    muy_frecuentes_sub.append((i.lower(), cont))

                '''frecuentes'''
                if 108 > dic_frecuencia_sub[i.lower()] > 31:
                    frecuentes_sub.append((i.lower(), cont))

                '''poco frecuentes'''
                if dic_frecuencia_sub[i.lower()] <= 31:
                    poco_frecuentes_sub.append((i.lower(), cont))

            cont += 1  # aumentamos el indice de la palabra

        self.started2.emit(95)

        muy_frecuentes = []  # palabras muy frecuentes en base al corpues CREA
        frecuentes = []  # palabras frecuentes en base al corpues CREA
        poco_frecuentes = []  # palabras poco frecuentes en base al corpues CREA

        '''rellenamos el json con la informacion por oracion'''
        sentence = 1
        fjson["Sentences_Set"] = []
        cont2 = 0
        for i in frases:
            wordsjson = []
            words_temp = word_tokenize(i, "spanish")
            for p in words_temp:
                if p.lower() in dic_frecuencia:
                    valor = ""
                    if dic_frecuencia[p.lower()] >= 4:
                        muy_frecuentes.append((p.lower(), cont2))
                        valor = "es muy frecuente"
                    if 4 > dic_frecuencia[p.lower()] > 1:
                        frecuentes.append((p.lower(), cont2))
                        valor = "es frecuente"
                    if dic_frecuencia[p.lower()] <= 1:
                        poco_frecuentes.append((p.lower(), cont2))
                        valor = "es poco frecuente"
                    wordsjson.append({
                        "Word": p + "",
                        "Frequency_value": dic_frecuencia[p.lower()],
                        "Results": valor
                    })
                else:
                    desconocidas.append((p.lower(), cont2))
                    wordsjson.append({
                        "Word": p + "",
                        "Frequency_value": None,
                        "Results": "no se encuentra en nuestro archivo. Valora que no exista o que sea una errata o "
                                   "un signo de puntuación "
                    })
                cont2 += 1
            fjson['Sentences_Set'].append({
                'Sentence_number': sentence,
                'Sentence': i + "",
                'mu_Index': legibilidad.mu(i),
                'Flesch-kincaid_index': textstat.flesch_kincaid_grade(i),
                'Words': wordsjson
            })

            sentence += 1

        resultados = [("Resultado: ", "")]

        '''calculamos los porcentajes de las variables anteriores para ser implementadas en el clasificador'''
        participle_verbs_number = (len(verbp) * 100) / lenwords
        preposition_number = (len(preposition) * 100) / lenwords
        por_comillas = (len(comillas) * 100) / lenwords
        por_frec = (len(frecuentes) * 100) / len(words)
        por_presente_indicativo = (len(presente_indicativo) * 100) / lenwords
        por_comas = (len(comas) * 100) / lenwords
        por_noun = (len(noun) * 100) / lenwords
        por_largas = (len(large) * 100) / lenwords
        por_muy_frecuentes_sub = (len(muy_frecuentes_sub) * 100) / lenwords
        documento = "vacio"

        '''almacenamos los resultados de las variables'''
        variables = [{
            "%Presente_Indicativo": por_presente_indicativo,
            "%Comillas": por_comillas,
            "#Frases": len(frases),
            "#Palabras": len(words),
            "%Comas": por_comas,
            "%Parciticipios": participle_verbs_number,
            "%Sustantivos": por_noun,
            "%Largas": por_largas,
            "%Muy_Frecuentes": por_muy_frecuentes_sub,
            "%Preposiciones": preposition_number,
            "%Frecuentes": por_frec
        }]

        dic_resultados = {}

        '''implementamos el clasificador para saber si un documento es facil o dificil'''
        if por_presente_indicativo <= 3.058824:
            resultados.append(("indicativo", por_presente_indicativo))
            dic_resultados["indicativo"] = verbos_no_indicativo
            if por_comillas <= 0.280767:
                resultados.append(("comillas", por_comillas))
                dic_resultados["comillas"] = comillas
                if len(frases) <= 34:
                    resultados.append(("#Frases", len(frases)))
                    documento = "Dificil"
                if len(frases) > 34:
                    if len(frases) <= 37:
                        resultados.append(("#Frases", len(frases)))
                        documento = "Facil"
                    if len(frases) > 37:
                        resultados.append(("#Frases", len(frases)))
                        documento = "Dificil"
            if por_comillas > 0.280767:
                resultados.append(("comillas", por_comillas))
                documento = "Dificil"
        if por_presente_indicativo > 3.058824:
            dic_resultados["indicativo"] = verbos_no_indicativo
            resultados.append(("indicativo", por_presente_indicativo))
            if len(words) <= 489:
                resultados.append(("palabras", len(words)))
                if por_comas <= 6.621773:
                    resultados.append(("comas", por_comas))
                    dic_resultados["comas"] = comas
                    if len(words) <= 306:
                        documento = "Dificil"
                    if len(words) > 306:
                        if participle_verbs_number <= 0.974026:
                            dic_resultados["participio"] = verbp
                            resultados.append(("participio", participle_verbs_number))
                            documento = "Facil"
                        if participle_verbs_number > 0.974026:
                            dic_resultados["participio"] = verbp
                            if por_noun <= 29.320988:
                                dic_resultados["sustantivos"] = noun
                                resultados.append(("sustantivos", por_noun))
                                documento = "Dificil"
                            if por_noun > 29.320988:
                                dic_resultados["sustantivos"] = noun
                                resultados.append(("sustantivos", por_noun))
                                documento = "Facil"
                if por_comas > 6.621773:
                    resultados.append(("comas", por_comas))
                    documento = "Facil"
                    dic_resultados["comas"] = comas
            if len(words) > 489:
                resultados.append(("palabras", len(words)))
                if por_largas <= 7.234043:
                    dic_resultados["largas"] = large
                    resultados.append(("largas", por_largas))
                    if por_muy_frecuentes_sub <= 68.782161:
                        dic_resultados["muy_frec"] = muy_frecuentes_sub
                        resultados.append(("muy_frec", por_muy_frecuentes_sub))
                        if preposition_number <= 14.554637:
                            dic_resultados["preposiciones"] = preposition
                            resultados.append(("preposiciones", preposition_number))
                            documento = "Facil"
                        if preposition_number > 14.554637:
                            resultados.append(("preposiciones", preposition_number))
                            dic_resultados["preposiciones"] = preposition
                            if por_comillas <= 0.214823:
                                dic_resultados["comillas"] = comillas
                                resultados.append(("comillas", por_comillas))
                                if por_frec <= 3.342618:
                                    dic_resultados["frecuentes"] = frecuentes
                                    resultados.append(("frecuentes", por_frec))
                                    documento = "Facil"
                                if por_frec > 3.342618:
                                    resultados.append(("frecuentes", por_frec))
                                    dic_resultados["frecuentes"] = frecuentes
                                    documento = "Dificil"
                            if por_comillas > 0.214823:
                                resultados.append(("comillas", por_comillas))
                                documento = "Dificil"
                    if por_muy_frecuentes_sub > 68.782161:
                        dic_resultados["muy_frecuente_sub"] = muy_frecuentes_sub
                        resultados.append(("muy_frecuente_sub", por_muy_frecuentes_sub))
                        documento = "Facil"
                if por_largas > 7.234043:
                    dic_resultados["largas"] = large
                    resultados.append(("largas", por_largas))
                    if por_presente_indicativo <= 4.41989:
                        resultados.append(("indicativo", por_presente_indicativo))
                        documento = "Dificil"
                        dic_resultados["indicativo"] = verbos_no_indicativo
                    if por_presente_indicativo > 4.41989:
                        resultados.append(("indicativo", por_presente_indicativo))
                        documento = "Facil"
                        dic_resultados["indicativo"] = verbos_no_indicativo

        '''alamcenamos si el texto es facil o dificil en un array con los resultados'''
        resultados[0] = ("Resumen", documento)

        '''terminamos de rellenar el json'''
        fjson['Readability_Analysis_Set'] = ({
            "Sentences_number": len(frases),
            "Words_number": lenwords,
            "Verbs_Number_set": [
                {
                    "Infinitive_Verbs_number": len(verbi),
                    "Gerund_Verbs_number": len(verbg),
                    "Participle_Verbs_number": len(verbp)
                }
            ],
            "Articles_number": len(determiner),
            "Preposition_number": len(preposition),
            "Dates_number": len(date),
            "Own_name_number": len(proper_noun),
            "Percentage_desconocidas": (len(desconocidas) * 100) / lenwords,
            "Result": documento,
            "Vars": variables
        })
        self.started2.emit(100)

        '''cremos un diccionario que guarde en cada clave los resultados'''
        dic_resultados2 = {'resultados': resultados, 'json': fjson, 'titulo': self.title, 'texto': self.text}

        self.final_signal.emit(dic_resultados, dic_resultados2)  # enviamos los resultados

    def stop(self):
        self.is_running = False
        self.terminate()
