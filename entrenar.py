import codecs
import math
import pickle
import string
import enchant
import nltk
import nltk.data
import dic as dic
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from PySide6.QtCore import QThread, QObject, Signal
import csv


class EntrenarCsv:


    def __init__(self, text, directory, title, tipo):
        self.text = text
        self.directory = directory
        self.title = title
        self.tipo = tipo

    def process(self):

        tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        frases = sent_tokenize(self.text, "spanish")
        words = word_tokenize(self.text, "spanish")
        freq = nltk.FreqDist(words)
        punct = string.punctuation
        freq2 = []
        for i in freq:
            if i not in punct:
                freq2.append((i, freq[i]))

        i1 = 0
        especifico = []
        general = []
        for item in freq2:
            if item[1] == 1:
                i1 += 1
        pt = ((math.sqrt(1 + 8 * i1) - 1) / 2)
        for item in freq2:
            if item[1] >= pt:
                general.append(item[0])
            else:
                especifico.append(item[0])

        caracteres = 0
        for i in words:
            caracteres += len(i)

        '''obtenemos los diccionarios que vamos a utilizar en el texto'''
        dic_frecuencia = dic.diccionario_frecuencia()
        dic_frecuencia_sub = dic.diccionario_frecuencia_sub()
        dic_sinonimos = dic.diccionario_sinonimos()
        dic_abreviaturas = dic.diccionario_abreviaturas()
        dic_siglas = dic.diccionario_siglas()
        dic_hom = dic.diccionario_homonimas()
        diccionario = dic.diccionario_freeling()
        dicEnchant = enchant.Dict("es_ES")

        entrada = open('diccionarios/etiquetador-spa.pkl', 'rb')
        etiquetador = pickle.load(entrada)
        analisis, lenwords = dic.freeling(self.text)
        if lenwords == 0:
            analisis = etiquetador.tag(words)
            lenwords = len(words)
        entrada.close()

        etc = []
        abrv = []
        siglas = []
        homo = []
        sinonimos_usados = {}
        numeros = []
        errores = []
        large = []
        superlative = []
        adverbs = []
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
        imperative = []
        number = []
        date = []
        interjection = []
        desconocidas = []
        sinonimos = []
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
        muy_frecuentes_sub = []
        frecuentes_sub = []
        poco_frecuentes_sub = []
        mayus_no_sigla = []
        frecuencia = []
        ordinales = []
        date_mal = []
        romanos = []
        dos_puntos = []
        otro_idioma = []
        proper_noun = []
        futuro = []
        pasado = []

        for x in analisis:
            i = x[0]
            j = x[1]
            k = i
            if len(x) == 3:
                k = x[2]

            if dicEnchant.check(i.lower()) == False and dicEnchant.check(j.lower()) == False \
                    and i.lower() not in punct and i not in dic_siglas and i not in dic_abreviaturas:
                if not any(map(str.isdigit, i)):
                    if "_" in i:
                        itemp = i.split("_")
                        for item2 in itemp:
                            if not dicEnchant.check(item2):
                                otro_idioma.append((item2, cont))
                    else:
                        otro_idioma.append((i, cont))

            if "_" in i:
                siglas_temp = i.split("_")
                for sig in siglas_temp:
                    if sig.isupper() and i not in dic_siglas:
                        if sig.isupper() not in diccionario and 2 <= len(sig) <= 7:
                            f = codecs.open('diccionarios/siglas-final.txt', "a", "utf-8")
                            f.write(sig + ':' + sig + '\n')
                            f.close()
                            dic_siglas = dic.diccionario_siglas()
                        else:
                            if len(i) > 1:
                                mayus_no_sigla.append((sig, cont))

            if i.isupper() and i not in dic_siglas:
                if i.lower() not in diccionario and "_" not in i and 2 <= len(i) <= 7:
                    f = codecs.open('diccionarios/siglas-final.txt', "a", "utf-8")
                    f.write(i + ':' + i + '\n')
                    f.close()
                    dic_siglas = dic.diccionario_siglas()
                else:
                    if len(i) > 1:
                        mayus_no_sigla.append((i, cont))

            if "&" in i or "%" in i or "/" in i or "(" in i or ")" in i or "^" in i or "[" in i or "]" in i or "{" in i or "}" in i or "..." in i or "ª" in i:
                errores.append((i, cont))
            if "etc" in i:
                etc.append((i, cont))
            if len(i) > 10 and "_" not in i:
                large.append((i, cont))
            if j[0] == "A" and j[2] == "S":
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
            if i.lower() == "por_lo_tanto":
                con_complex.append((i, cont))
            if i.lower() == "no_obstante":
                con_complex.append((i, cont))
            if i.lower() == "por_consiguiente":
                con_complex.append((i, cont))
            if i.lower() == "sin" and analisis[cont + 1][0].lower() == "embargo":
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
                        t = t.replace("\n", "")
                        if t in sinonimos_usados:
                            if sinonimos_usados[t] == "" and t not in sinonimos:
                                sinonimos.append(t)
                            usado = 1
                            sinonimos_usados[t] += i + ", "
                            if i.lower() not in sinonimos:
                                sinonimos.append(i.lower())
                            sin.append(i)
                    if usado == 0:
                        sinonimos_usados[i] = ""

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
                if j[1] == "P":
                    proper_noun.append(i)
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
                if j[3] == "F":
                    futuro.append(i)
                if j[3] == "S":
                    pasado.append(i)
                if j[2] == "M":
                    imperative.append(i)
            if j[0] == "Z":
                number.append(i)
                if len(j) > 1:
                    if j[1] == "p" or j[1] == "d":
                        partitivos.append(i)
                if "º" in i:
                    ordinales.append((i, cont))
                if len(i) == 10:
                    barras = 0
                    guiones = 0
                    for tt in i:
                        if tt == "/":
                            barras += 1
                        if tt == "-":
                            guiones += 1
                    if barras == 2 and guiones == 0:
                        date_mal.append((i, cont))
                    if barras == 0 and guiones == 2:
                        date_mal.append((i, cont))
            if j == "W":
                date.append(i)
                if "/" in i:
                    date_mal.append((i, cont))
                if "I" in i or "V" in i or "X" in i or "L" in i or "C" in i or "D" in i or "M" in i:
                    romanos.append((i, cont))
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

            if j[0] != "F" and i not in frecuencia:
                frecuencia.append(i)

            if i.lower() in dic_frecuencia:
                if dic_frecuencia[i.lower()] >= 4:
                    muy_frecuentes.append(i.lower())
                if 4 > dic_frecuencia[i.lower()] > 1:
                    frecuentes.append(i.lower())
                if dic_frecuencia[i.lower()] <= 1:
                    poco_frecuentes.append(i.lower())
            else:
                desconocidas.append(i.lower())

            if i.lower() in dic_frecuencia_sub:
                if dic_frecuencia_sub[i.lower()] >= 108:
                    muy_frecuentes_sub.append(i.lower())
                if 108 > dic_frecuencia_sub[i.lower()] > 31:
                    frecuentes_sub.append(i.lower())
                if dic_frecuencia_sub[i.lower()] <= 31:
                    poco_frecuentes_sub.append(i.lower())

            cont += 1
        if len(verbs) == 0:
            verbs.append("")
        if len(noun) == 0:
            noun.append("")
        valores = [self.title,
                   (len(sin) * 100) / lenwords,
                   (len(abrv) * 100) / lenwords,
                   (len(siglas) * 100) / lenwords,
                   (len(verbs) * 100) / lenwords,
                   (len(verbi) * 100) / lenwords,
                   (len(verbg) * 100) / lenwords,
                   (len(verbp) * 100) / lenwords,
                   (len(imperative) * 100) / lenwords,
                   (len(determiner) * 100) / lenwords,
                   (len(preposition) * 100) / lenwords,
                   (len(noun) * 100) / lenwords,
                   (len(large) * 100) / lenwords,
                   (len(superlative) * 100) / lenwords,
                   (len(adverbs) * 100) / lenwords,
                   (len(adverb) * 100) / lenwords,
                   (len(errores) * 100) / lenwords,
                   (len(indeterminate) * 100) / lenwords,
                   (len(numeros) * 100) / lenwords,
                   (len(con_complex) * 100) / lenwords,
                   (len(muy_frecuentes) * 100) / lenwords,
                   (len(frecuentes) * 100) / lenwords,
                   (len(poco_frecuentes) * 100) / lenwords,
                   (len(muy_frecuentes_sub) * 100) / lenwords,
                   (len(frecuentes_sub) * 100) / lenwords,
                   (len(poco_frecuentes_sub) * 100) / lenwords,
                   (len(comillas) * 100) / lenwords,
                   (len(homo) * 100) / lenwords,
                   len(words) / len(frases),
                   caracteres / len(words),
                   (len(comas)) / len(frases),
                   (len(comas) * 100) / lenwords,
                   (len(puntos) * 100) / lenwords,
                   (len(punto_coma) * 100) / lenwords,
                   (len(date) * 100) / lenwords,
                   (len(date_mal) * 100) / lenwords,
                   (doble_negacion * 100) / lenwords,
                   (len(partitivos) * 100) / lenwords,
                   (len(presente_indicativo) * 100) / lenwords,
                   (len(presente_indicativo) * 100) / len(verbs),
                   (len(subjuntivo) * 100) / lenwords,
                   (len(condicional) * 100) / lenwords,
                   (nverbseguidos * 100) / lenwords,
                   (len(puntuacion) * 100) / lenwords,
                   (len(etc) * 100) / lenwords,
                   (len(mayus_no_sigla) * 100) / lenwords,
                   (len(sinonimos) * 100) / len(freq2),
                   (len(ordinales) * 100) / lenwords,
                   (len(romanos) * 100) / lenwords,
                   (len(general) * 100) / len(freq2),
                   (len(especifico) * 100) / len(freq2),
                   (len(dos_puntos) * 100) / lenwords,
                   (len(otro_idioma) * 100) / lenwords,
                   len(words),
                   len(frases),
                   (len(proper_noun) * 100) / lenwords,
                   (len(proper_noun) * 100) / len(noun),
                   (len(futuro) * 100) / lenwords,
                   (len(futuro) * 100) / len(verbs),
                   (len(pasado) * 100) / lenwords,
                   (len(pasado) * 100) / len(verbs),
                   self.tipo]

        with open(self.directory + '/entrenamiento.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(valores)

        print("Fin\n")
