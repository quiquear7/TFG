import codecs
import pickle
import nltk
import nltk.data
import dic as dic
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import csv


class EntrenarCsv:

    def __init__(self, text, directory, title, tipo):
        self.text = text
        self.directory = directory
        self.title = title
        self.tipo = tipo

    def process(self):

        """Conectamos con la base de datos"""
        # client = pymongo.MongoClient(
        # "mongodb+srv://quiquear7:tfg2021uc3m@tfg.ickp8.mongodb.net/BD_TFG?retryWrites=true&w=majority")
        # db = client.BD_TFG
        # collection = db.Docs

        tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        frases2 = tokenizer.tokenize(self.text)
        frases = sent_tokenize(self.text, "spanish")
        words = word_tokenize(self.text, "spanish")
        freq = nltk.FreqDist(words)

        '''obtenemos los diccionarios que vamos a utilizar en el texto'''
        dic_frecuencia = dic.diccionario_frecuencia()
        dic_frecuencia_sub = dic.diccionario_frecuencia_sub()
        dic_sinonimos = dic.diccionario_sinonimos()
        dic_abreviaturas = dic.diccionario_abreviaturas()
        dic_siglas = dic.diccionario_siglas()
        dic_hom = dic.diccionario_homonimas()
        diccionario = dic.diccionario_freeling()

        entrada = open('diccionarios/etiquetador-spa.pkl', 'rb')
        etiquetador = pickle.load(entrada)
        analisis, lenwords = dic.freeling(self.text)
        if lenwords == 0:
            analisis = etiquetador.tag(words)
            lenwords = len(words)
        entrada.close()

        abrv = []
        siglas = []
        homo = []
        sinonimos_usados = {}
        numeros = []
        errores = []
        large = []
        superlative = []
        adverbs = []
        title = []
        indeterminate = []
        numbers = []
        comillas = []
        con_complex = []
        presente_indicativo = []
        subjuntivo = []
        condicional = []
        adjective = []
        conjunction = []
        determiner = []
        noun = []
        pronoun = []
        adverb = []
        preposition = []
        verbs = []
        verbi = []
        verbg = []
        verbp = []
        number = []
        date = []
        interjection = []
        desconocidas = []
        sinonimos = []
        caracteres = 0
        nverbseguidos = 0
        puntos = []
        comas = []
        punto_coma = []
        doble_negacion = 0
        verbos_seguidos = []
        partitivos = []
        sin = []
        cont = 0
        cont_negative = 0
        negative_text = ""
        doble_negacion_array = []
        puntuacion = []
        muy_frecuentes = []
        frecuentes = []
        poco_frecuentes = []

        f = codecs.open('diccionarios/siglas-final.txt', "a", "utf-8")

        for x in analisis:
            i = x[0]
            j = x[1]
            k = i
            if len(x) == 3:
                k = x[2]

            caracteres += len(i)
            if i.isupper() and i not in dic_siglas and 2 <= len(i[0]) <= 7 and i.lower() not in diccionario:
                f.write(i + ':' + i + '\n')
                siglas.append((i, cont))
            if i == "&" or i == "%" or i == "/" or i == "(" or i == ")" or i == "^" or i == "[" or i == "]" or i == "{" or i == "}" or i == "etc." or i == "...":
                errores.append((i, cont))
            if len(i) > 10 and "_" not in i:
                large.append((i, cont))
            if j[0] == "A" and ("ísimo" in i or "érrimo" in i):
                superlative.append((i, cont))
            if j[0] == "R" and "mente" in i:
                adverbs.append((i, cont))
            if "@" in i:
                errores.append((i, cont))
            if i == "cosa" or i == "algo" or i == "asunto":
                indeterminate.append((i, cont))
            if ("º" in i or "ª" in i) or (j[0] == "M" and j[1] == "O"):
                numbers.append((i, cont))
            if '"' == i or "«" == i or "»" == i or "'" == i:
                comillas.append((i, cont))
            if i.isdigit():
                numeros.append((i, cont))
            if i == "por " and analisis[cont + 1][0] == "lo" and analisis[cont + 2][0] == "tanto":
                con_complex.append((i, cont))
            if i == "no " and analisis[cont + 1][0] == "obstante":
                con_complex.append((i, cont))
            if i == "por " and analisis[cont + 1][0] == "consiguiente":
                con_complex.append((i, cont))
            if i == "sin " and analisis[cont + 1][0] == "embargo":
                con_complex.append((i, cont))

            if i in dic_abreviaturas:
                abrv.append(i)
            if i in dic_siglas:
                siglas.append(i)
            if i in dic_hom:
                homo.append(i)

            if k not in sinonimos_usados:
                if k in dic_sinonimos:
                    x = dic_sinonimos[k]
                    usado = 0
                    for t in x:
                        t = t.replace(",", "")
                        if t in sinonimos_usados:
                            usado = 1
                            sinonimos_usados[t] += i + ", "
                            sinonimos.append(k)
                            sin.append(k)
                    if usado == 0:
                        sinonimos_usados[k] = ""
            else:
                sinonimos_usados[k] = ""

            if "_" in i:
                z = i.split("_")
                for t in z:
                    if t in dic_abreviaturas:
                        abrv.append(i)
                    if t in dic_siglas:
                        siglas.append(i)

            if j[0] == "A":
                adjective.append(i)
            if j[0] == "C":
                conjunction.append(i)
            if j[0] == "D":
                determiner.append(i)
            if j[0] == "N":
                noun.append(i)
            if j[0] == "P":
                pronoun.append(i)
            if j[0] == "R":
                adverb.append(i)
                if j[1] == "N":
                    cont_negative += 1
                    negative_text += i + "-"
            if "ningun" in i or "ningún" in i:
                cont_negative += 1
                negative_text += i + "-"
            if j[0] == "V":
                verbs.append(i)
                if analisis[cont + 1][1][0] == "V":
                    verbos_seguidos.append((i, analisis[cont + 1][0]))
                    nverbseguidos += 2
                if j[2] == "N":
                    verbi.append(i)
                if j[2] == "G":
                    verbg.append(i)
                if j[2] == "P":
                    verbp.append(i)
                if j[2] == "I" and j[3] == "P":
                    presente_indicativo.append(i)
                if j[2] == "S":
                    subjuntivo.append(i)
                if j[3] == "C":
                    condicional.append(i)
            if j[0] == "Z":
                number.append(i)
                if len(j) > 1:
                    if j[1] == "p" or j[1] == "d":
                        partitivos.append(i)
            if j == "W":
                date.append(i)
            if j[0] == "Yo":
                interjection.append(i)
            if j == "SP":
                preposition.append(i)

            if j == "Fc":
                comas.append(j)
            if j == "Fp":
                if cont_negative > 1:
                    doble_negacion += 1
                    doble_negacion_array.append(negative_text)
                cont_negative = 0
                negative_text = ""
                puntos.append(j)
            if j == "Fx":
                punto_coma.append(j)

            if j[0] == "F":
                puntuacion.append(j)

            if i.lower() in dic_frecuencia:
                if dic_frecuencia[i.lower()] >= 4:
                    muy_frecuentes.append(i.lower())
                if 4 > dic_frecuencia[i.lower()] > 0.3:
                    frecuentes.append(i.lower())
                if dic_frecuencia[i.lower()] <= 0.3:
                    poco_frecuentes.append(i.lower())
            else:
                desconocidas.append(i.lower())

            cont += 1
        f.close()

        # client.close()
        valores = [self.title,
                   (len(sinonimos) * 100) / lenwords,
                   (len(abrv) * 100) / lenwords,
                   (len(siglas) * 100) / lenwords,
                   (len(verbs) * 100) / lenwords,
                   (len(verbi) * 100) / lenwords,
                   (len(verbg) * 100) / lenwords,
                   (len(verbp) * 100) / lenwords,
                   (len(determiner) * 100) / lenwords,
                   (len(preposition) * 100) / lenwords,
                   (len(noun) * 100) / lenwords,
                   (len(desconocidas) * 100) / lenwords,
                   (len(large) * 100) / lenwords,
                   (len(superlative) * 100) / lenwords,
                   (len(adverb) * 100) / lenwords,
                   (len(errores) * 100) / lenwords,
                   (len(indeterminate) * 100) / lenwords,
                   (len(numeros) * 100) / lenwords,
                   (len(con_complex) * 100) / lenwords,
                   (len(muy_frecuentes) * 100) / lenwords,
                   (len(frecuentes) * 100) / lenwords,
                   (len(poco_frecuentes) * 100) / lenwords,
                   (len(comillas) * 100) / lenwords,
                   (len(homo) * 100) / lenwords,
                   lenwords / len(frases),
                   caracteres / lenwords,
                   (len(comas)) / len(frases),
                   (len(comas) * 100) / lenwords,
                   (len(puntos) * 100) / lenwords,
                   (len(punto_coma) * 100) / lenwords,
                   (len(date) * 100) / lenwords,
                   (doble_negacion * 100) / lenwords,
                   (len(partitivos) * 100) / lenwords,
                   (len(presente_indicativo) * 100) / lenwords,
                   (len(subjuntivo) * 100) / lenwords,
                   (len(condicional) * 100) / lenwords,
                   (nverbseguidos * 100) / lenwords,
                   (len(puntuacion) * 100) / lenwords,
                   self.tipo]

        with open(self.directory + '/final_v31.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(valores)

        print("Fin\n")
