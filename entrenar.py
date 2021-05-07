import codecs
import pickle
import nltk
import nltk.data
import dic as dic
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from legibilidad import legibilidad
import textstat
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

        """obtenemos el título del documento"""
        '''Rellenamos json'''
        fjson = {
            "Title": self.title,
            "URL": "",
            "Format": "csv",
            "Topic": "",
            "Aimed_to": "",
            "Character": "",
            'Readability_Set': {
                'mu_Index': legibilidad.mu(self.text),
                'Flesch-kincaid_index': textstat.flesch_kincaid_grade(self.text)
            }
        }

        tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        frases2 = tokenizer.tokenize(self.text)
        frases = sent_tokenize(self.text, "spanish")
        words = word_tokenize(self.text, "spanish")
        freq = nltk.FreqDist(words)
        # print("freq: ", freq.items())

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
        upper = []
        errores = []
        large = []
        superlative = []
        adverbs = []
        title = []
        indeterminate = []
        numbers = []
        date = []
        comillas = []
        con_complex = []

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

        puntos = []
        comas = []
        punto_coma = []

        cont = 0
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
            if len(i) > 13:
                large.append((i, cont))
            if j[0] == "A" and ("ísimo" in i or "érrimo" in i):
                superlative.append((i, cont))
            if j[0] == "R" and "mente" in i:
                adverbs.append((i, cont))
            if "@" in i:
                errores.append((i, cont))
            '''if cont < lenwords - 1:
                if i == "." and analisis[cont + 1][0].istitle() is False and analisis[cont + 1][0].isdigit() is False:
                    title.append((words[cont + 1], cont))'''
            if i == "cosa" or i == "algo" or i == "asunto":
                indeterminate.append((i, cont))
            if ("º" in i or "ª" in i) or (j[0] == "M" and j[1] == "O"):
                numbers.append((i, cont))
            if '"' == i:
                comillas.append((i, cont))
            if i.isdigit():
                numeros.append((i, cont))
            if i == "por " and words[cont + 1] == "lo" and words[cont + 2] == "tanto":
                con_complex.append((i, cont))
            if i == "no " and words[cont + 1] == "obstante":
                con_complex.append((i, cont))
            if i == "por " and words[cont + 1] == "consiguiente":
                con_complex.append((i, cont))
            if i == "sin " and words[cont + 1] == "embargo":
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
                    if usado == 0:
                        sinonimos_usados[k] = ""
            else:
                sinonimos_usados[k] = ""

            if j == "Fc":
                comas.append(j)
            if j == "Fp":
                puntos.append(j)
            if j == "Fx":
                punto_coma.append(j)

            existe = 1
            if "_" in i:
                z = i.split("_")
                for t in z:
                    if t not in dic_frecuencia:
                        existe = 0
                    if t in dic_abreviaturas:
                        abrv.append(i)
                    if t in dic_siglas:
                        siglas.append(i)

            if (dic_frecuencia.get(i.lower())) or ("_" in i and existe == 1) or j[0] == "F":
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
                if j[0] == "V":
                    verbs.append(i)
                    if j[2] == "N":
                        verbi.append(i)
                    if j[2] == "G":
                        verbg.append(i)
                    if j[2] == "P":
                        verbp.append(i)
                if j[0] == "Z":
                    number.append(i)
                if j[0] == "W":
                    date.append(i)
                if j[0] == "Yo":
                    interjection.append(i)
                if j == "SP":
                    preposition.append(i)
            else:
                desconocidas.append(i)

            cont += 1
        f.close()
        # (upper)
        # print(errores)
        # print(large)
        # print(superlative)
        # print(adverbs)
        # print(arroba)
        # print(title)
        # print(indeterminate)
        # print(numbers)

        muy_frecuentes = []
        frecuentes = []
        poco_frecuentes = []

        '''for i in clean:
            for syn in wordnet.synsets(i):
                print("significado:" + i + " ----" + syn.definition())'''

        sentence = 1
        fjson["Sentences_Set"] = []
        for i in frases:
            wordsjson = []
            words_temp = word_tokenize(i, "spanish")
            for p in words_temp:
                if p.lower() in dic_frecuencia:
                    valor = ""
                    if dic_frecuencia[p.lower()] >= 1:
                        muy_frecuentes.append(p.lower())
                        valor = "es muy frecuente"
                    if 1 > dic_frecuencia[p.lower()] > 0.3:
                        frecuentes.append(p.lower())
                        valor = "es frecuente"
                    if dic_frecuencia[p.lower()] <= 0.3:
                        poco_frecuentes.append(p.lower())
                        valor = "es poco frecuente"
                    wordsjson.append({
                        "Word": p + "",
                        "Frequency_value": dic_frecuencia[p.lower()],
                        "Results": valor
                    })
                else:
                    wordsjson.append({
                        "Word": p + "",
                        "Frequency_value": None,
                        "Results": "no se encuentra en nuestro archivo. Valora que no exista o que sea una errata o "
                                   "un signo de puntuación "
                    })

            fjson['Sentences_Set'].append({
                'Sentence_number': sentence,
                'Sentence': i + "",
                'mu_Index': legibilidad.mu(i),
                'Flesch-kincaid_index': textstat.flesch_kincaid_grade(i),
                'Words': wordsjson
            })

            sentence += 1

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
            "Own_name_number": len(noun),
            "Percentage_desconocidas": (len(desconocidas) * 100) / lenwords
        })

        # collection.insert_one(fjson)
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
                   (len(adverbs) * 100) / lenwords,
                   (len(errores) * 100) / lenwords,
                   (len(upper) * 100) / lenwords,
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
                   (len(puntos)) / len(frases),
                   (len(punto_coma)) / len(frases),
                   len(frases),
                   self.tipo]

        with open(self.directory+'/final_v18.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(valores)

        print("Fin\n")
