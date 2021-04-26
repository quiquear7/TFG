import codecs
import pickle
import string

import nltk
import nltk.data
import pymongo

import dic as dic
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.corpus import cess_esp
from nltk.corpus.reader import XMLCorpusReader
from datetime import datetime
from legibilidad import legibilidad
import textstat
import json


class Pln:

    def __init__(self, text, directory, title, url):
        self.text = text
        self.directory = directory
        self.title = title
        self.url = url

    def process(self):

        """Conectamos con la base de datos"""
        # client = pymongo.MongoClient("mongodb+srv://quiquear7:tfg2021uc3m@tfg.ickp8.mongodb.net/BD_TFG?retryWrites
        # =true&w=majority") db = client.BD_TFG collection = db.Docs

        """obtenemos el título del documento"""
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

        tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        frases = tokenizer.tokenize(self.text)
        frases = sent_tokenize(self.text, "spanish")
        words = word_tokenize(self.text, "spanish")

        freq = nltk.FreqDist(words)
        # print("freq: ", freq.items())

        clean = frases[:]
        sr = stopwords.words('spanish')
        for token in frases:
            if token in sr:
                clean.remove(token)

        '''obtenemos los diccionarios que vamos a utilizar en el texto'''
        palabras = dic.diccionario_palabras()
        dic_frecuencia = dic.diccionario_frecuencia()
        dic_sinonimos = dic.diccionario_sinonimos()
        dic_abreviaturas = dic.diccionario_abreviaturas()
        dic_siglas = dic.diccionario_siglas()
        dic_hom = dic.diccionario_homonimas()
        diccionario = dic.diccionario_freeling()

        sigla = []
        f = codecs.open('diccionarios/siglas-final.txt', "a", "utf-8")
        for i in freq.items():
            if i[0].isupper() and int(i[1]) > 1 and 2 <= len(i[0]) <= 5:
                if i[0] not in dic_abreviaturas:
                    f.write(i[0] + ':' + i[0] + '\n')
                    sigla.append(i[0])
        f.close()

        '''spanish_stemmer = SnowballStemmer('spanish')
        for i in words:
            print(spanish_stemmer.stem(i), end='\n')
            print("\n")'''

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
        for x in analisis:

            i = x[0]
            j = x[1]

            caracteres += len(i)
            if i.isupper() and i not in dic_siglas:
                upper.append(i)
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
            if cont < len(words) - 1:
                if i == "." and words[cont + 1].istitle() is False and words[cont + 1].isdigit() is False:
                    title.append((words[cont + 1], cont))
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

            i = i.lower()
            if i not in sinonimos_usados:
                if i in dic_sinonimos:
                    x = dic_sinonimos[i]
                    for t in x:
                        t = t.replace(",", "")
                        if t in sinonimos_usados:
                            sinonimos_usados[t] += i + ", "
                            sinonimos.append(i)
            else:
                sinonimos_usados[i] = ""

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

        # print(upper)
        # print(errores)
        # print(large)
        # print(superlative)
        # print(adverbs)
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
                    if dic_frecuencia[p.lower()] >= 0.4:
                        muy_frecuentes.append(p.lower())
                        valor = "es muy frecuente"
                    if 0.4 > dic_frecuencia[p.lower()] > 0.2:
                        frecuentes.append(p.lower())
                        valor = "es frecuente"
                    if dic_frecuencia[p.lower()] <= 0.2:
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

        resultados = []

        resultados.append(("Resultado: ", ""))

        N_sentences = len(frases)
        resultados.append(("N_sentences", N_sentences))

        Comas = (len(comas)) / len(frases)
        resultados.append(("Comas", Comas))

        Participle_Verbs_number = (len(verbp) * 100) / lenwords
        resultados.append(("Participle_Verbs_number", Participle_Verbs_number))

        Por_Abreviaturas = (len(abrv) * 100) / lenwords
        resultados.append(("Por_Abreviaturas", Por_Abreviaturas))

        Ratio_Caracteres_Palabra = caracteres / lenwords
        resultados.append(("Ratio_Caracteres_Palabra", Ratio_Caracteres_Palabra))

        Por_Simbolos = (len(errores) * 100) / lenwords
        resultados.append(("Por_Simbolos", Por_Simbolos))

        Preposition_number = (len(preposition) * 100) / lenwords
        resultados.append(("Preposition_number", Preposition_number))

        Infinitive_Verbs_number = (len(verbi) * 100) / lenwords
        resultados.append(("Infinitive_Verbs_number", Infinitive_Verbs_number))

        Determiners_number = (len(determiner) * 100) / lenwords
        resultados.append(("Determiners_number", Determiners_number))

        Por_Sinonimos = (len(sinonimos) * 100) / lenwords
        resultados.append(("Por_Sinonimos", Por_Sinonimos))

        Por_comillas = (len(comillas) * 100) / lenwords
        resultados.append(("Por_comillas", Por_comillas))

        Por_verbs = (len(verbs) * 100) / lenwords
        resultados.append(("Por_verbs", Por_verbs))

        N_puntos = (len(puntos)) / len(frases)
        resultados.append(("N_puntos", N_puntos))

        documento = "vacio"

        if N_sentences <= 24:
            if Comas <= 0.6:
                documento = "Dificil"
            if Comas > 0.6:
                if N_sentences <= 5:
                    documento = "Dificil"
                if N_sentences > 5:
                    if Participle_Verbs_number <= 1.183432:
                        if Por_Abreviaturas <= 2.287582:
                            documento = "Facil"
                        if Por_Abreviaturas > 2.287582:
                            documento = "Dificil"
                    if Participle_Verbs_number > 1.183432:
                        if Ratio_Caracteres_Palabra <= 4.760141:
                            if Por_Simbolos <= 0.93633:
                                documento = "Dificil"
                            if Por_Simbolos > 0.93633:
                                documento = "Facil"
                        if Ratio_Caracteres_Palabra > 4.760141:
                            if Participle_Verbs_number <= 2.754237:
                                if Participle_Verbs_number <= 1.731602:
                                    documento = "Dificil"
                                if Participle_Verbs_number > 1.731602:
                                    if Preposition_number <= 14.814815:
                                        documento = "Facil"
                                    if Preposition_number > 14.814815:
                                        if Infinitive_Verbs_number <= 4.850746:
                                            if Determiners_number <= 12.418906:
                                                if Por_Sinonimos <= 2.517623:
                                                    documento = "Facil"
                                                if Por_Sinonimos > 2.517623:
                                                    documento = "Dificil"
                                            if Determiners_number > 12.418906:
                                                documento = "Dificil"
                                        if Infinitive_Verbs_number > 4.850746:
                                            documento = "Facil"
                                if Participle_Verbs_number > 2.754237:
                                    documento = "Dificil"
        if N_sentences > 24:
            if Por_comillas <= 0:
                if Por_verbs <= 9.968354:
                    if N_puntos <= 0.942857:
                        documento = "Facil"
                    if N_puntos > 0.942857:
                        documento = "Dificil"
                if Por_verbs > 9.968354:
                    documento = "Facil"
            if Por_comillas > 0:
                documento = "Dificil"
        print(documento)

        resultados[0] = ("Resumen", documento)

        fjson['Readability_Analysis_Set'] = ({
            "Sentences_number": len(frases),
            "Words_number": len(words),
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
            "Percentage_desconocidas": (len(desconocidas) * 100) / len(words),
            "Resumen": documento
        })

        n_sin = 0
        for i in sinonimos_usados.values():
            if i != "":
                n_sin += 1

        # print(sinonimos_usados)
        # print("Porcentaje de Sinonimos: ", (n_sin * 100) / len(words))
        # print(abrv)
        # print("Porcentaje de Abreviaturas: ", (len(abrv) * 100) / len(words))
        # print(siglas)
        # print("Porcentaje de Siglas: ", (len(siglas) * 100) / len(words))
        # print(homo)
        # print("Porcentaje de Homonimas: ", (len(homo) * 100) / len(words))

        # collection.insert_one(fjson)
        # client.close()
        ajson = self.directory + '/' + self.title + '.json'
        # with open(ajson, 'w', encoding='utf8') as file:
        # json.dump(fjson, file, ensure_ascii=False, indent=4)

        print("Fin\n")
        return resultados, fjson, self.title
