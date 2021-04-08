import codecs
import pickle
import string

import nltk
import nltk.data

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

    def __init__(self, text, directory, title):
        self.text = text
        self.directory = directory
        self.title = title

    def process(self):

        """obtenemos el título del documento"""
        punct = string.punctuation
        for c in punct:
            self.title = self.title.replace(c, "")

        palabras = self.title.split()
        titulo = ""
        for i in palabras:
            if i[0].isalnum():
                titulo += i[0].capitalize()

        '''Rellenamos json'''
        fjson = {
            "Title": titulo,
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
        frases = tokenizer.tokenize(self.text)
        frases2 = sent_tokenize(self.text, "spanish")
        words = word_tokenize(self.text, "spanish")

        freq = nltk.FreqDist(words)
        print("freq: ", freq.items())

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

        entrada = open('etiquetador-spa.pkl', 'rb')
        etiquetador = pickle.load(entrada)
        entrada.close()
        analisis = etiquetador.tag(words)
        print(analisis)

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
        arroba = []
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
        verbi = []
        verbg = []
        verbp = []
        number = []
        date = []
        interjection = []
        desconocidas = []

        cont = 0
        for x in analisis:
            i = x[0]
            j = x[1]
            if i.isupper() and i not in dic_siglas:
                upper.append(i)
            if i == ";" or i == "&" or i == "%" or i == "/" or i == "(" or i == ")" or i == "^" or i == "[" or i == "]" or i == "{" or i == "}" or i == "etc." or i == "...":
                errores.append((i, cont))
            if len(i) > 13:
                large.append((i, cont))
            if j[0] == "A" and ("ísimo" in i or "érrimo" in i):
                superlative.append((i, cont))
            if j[0] == "R" and "mente" in i:
                adverbs.append((i, cont))
            if "@" in i:
                arroba.append((i, cont))
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
                    usado = 0
                    for t in x:
                        t = t.replace(",", "")
                        if t in sinonimos_usados:
                            usado = 1
                            sinonimos_usados[t] += i + ", "
                    if usado == 0:
                        sinonimos_usados[i] = ""
            else:
                sinonimos_usados[i] = ""

            if i.lower() in palabras or i.lower in diccionario:
                info = diccionario[i.lower()]
                et = info.split()

                if et[1][0] == "A":
                    adjective.append(et[0])
                if et[1][0] == "C":
                    conjunction.append(et[0])
                if et[1][0] == "D":
                    determiner.append(et[0])
                if et[1][0] == "N":
                    noun.append(et[0])
                if et[1][0] == "P":
                    pronoun.append(et[0])
                if et[1][0] == "R":
                    adverb.append(et[0])
                if et[1][0] == "V":
                    if et[1][2] == "N":
                        verbi.append(et[0])
                    if et[1][2] == "G":
                        verbg.append(et[0])
                    if et[1][2] == "P":
                        verbp.append(et[0])
                if et[1][0] == "Z":
                    number.append(et[0])
                if et[1][0] == "W":
                    date.append(et[0])
                if et[1][0] == "Yo":
                    interjection.append(et[0])
                if et[1][0] == "S":
                    preposition.append(et[0])
            else:
                desconocidas.append(i)

            cont += 1
        print(upper)
        print(errores)
        print(large)
        print(superlative)
        print(adverbs)
        print(arroba)
        print(title)
        print(indeterminate)
        print(numbers)

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
                    if dic_frecuencia[p.lower()] >= 0.3:
                        valor = "es muy frecuente"
                    if 0.3 > dic_frecuencia[p.lower()] > 0.1:
                        valor = "es frecuente"
                    if dic_frecuencia[p.lower()] <= 0.1:
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
                        "Results": "no se encuentra en nuestro archivo. Valora que no exista o que sea una errata o un signo de puntuación"
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
            "Percentage_desconocidas": (len(desconocidas) * 100) / len(words)
        })

        n_sin = 0
        for i in sinonimos_usados.values():
            if i != "":
                n_sin += 1

        print(sinonimos_usados)
        print("Porcentaje de Sinonimos: ", (n_sin * 100) / len(words))
        print(abrv)
        print("Porcentaje de Abreviaturas: ", (len(abrv) * 100) / len(words))
        print(siglas)
        print("Porcentaje de Siglas: ", (len(siglas) * 100) / len(words))
        print(homo)
        print("Porcentaje de Homonimas: ", (len(homo) * 100) / len(words))

        ajson = self.directory + '/' + titulo + '.json'

        with open(ajson, 'w', encoding='utf8') as file:
            json.dump(fjson, file, ensure_ascii=False, indent=4)

        print("Fin")
