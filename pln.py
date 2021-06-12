import codecs
import math
import pickle
import string
import enchant
import nltk
import nltk.data
from PySide6.QtCore import QThread, QObject

import dic as dic
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from legibilidad import legibilidad
import textstat


class Pln:

    def __init__(self, text, title, url):
        self.text = text
        self.title = title
        self.url = url

    def process(self):
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
        muy_frecuentes_sub = []
        frecuentes_sub = []
        poco_frecuentes_sub = []
        mayus_no_sigla = []
        frecuencia = []
        ordinales = []
        date_mal = []
        romanos = []
        otro_idioma = []
        verbos_no_indicativo = []

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
                abrv.append((i, cont))
            if i in dic_siglas:
                siglas.append((i, cont))
            if i in dic_hom:
                homo.append((i, cont))

            if k not in sinonimos_usados:
                if k in dic_sinonimos:
                    x = dic_sinonimos[k]
                    usado = 0
                    for t in x:
                        t = t.replace(",", "")
                        t = t.replace("\n", "")
                        if t in sinonimos_usados:
                            if sinonimos_usados[t] == "" and t not in sinonimos:
                                sinonimos.append((t, cont))
                            usado = 1
                            sinonimos_usados[t] += i + ", "
                            if i.lower() not in sinonimos:
                                sinonimos.append((i.lower(), cont))
                            sin.append((i, cont))
                    if usado == 0:
                        sinonimos_usados[k] = ""

            if "_" in i:
                z = i.split("_")
                for t in z:
                    if t in dic_abreviaturas:
                        abrv.append((t, cont))
                    if t in dic_siglas:
                        siglas.append((t, cont))

            if j[0] == "A":
                adjective.append((i, cont))
            if j[0] == "C":
                conjunction.append((i, cont))
            if j[0] == "D":
                determiner.append((i, cont))
            if j[0] == "N":
                noun.append((i, cont))
            if j[0] == "P":
                pronoun.append((i, cont))
            if j[0] == "R":
                adverb.append((i, cont))
                if j[1] == "N":
                    cont_negative += 1
                    negative_text += i + "-"
            if "ningun" in i or "ningún" in i:
                cont_negative += 1
                negative_text += i + "-"
            if j[0] == "V":
                verbs.append((i, cont))
                if analisis[cont + 1][1][0] == "V":
                    verbos_seguidos.append((i, analisis[cont + 1][0]))
                    nverbseguidos += 2
                if j[2] == "N":
                    verbi.append((i, cont))
                if j[2] == "G":
                    verbg.append((i, cont))
                if j[2] == "P":
                    verbp.append((i, cont))
                if j[2] == "I" and j[3] == "P":
                    presente_indicativo.append((i, cont))
                if j[2] != "I":
                    verbos_no_indicativo.append((i, cont))
                if j[2] == "S":
                    subjuntivo.append((i, cont))
                if j[3] == "C":
                    condicional.append((i, cont))
                if j[2] == "M":
                    imperative.append((i, cont))
            if j[0] == "Z":
                number.append(i)
                if len(j) > 1:
                    if j[1] == "p" or j[1] == "d":
                        partitivos.append((i, cont))
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
                date.append((i, cont))
                if "/" in i:
                    date_mal.append((i, cont))
                if "I" in i or "V" in i or "X" in i or "L" in i or "C" in i or "D" in i or "M" in i:
                    romanos.append((i, cont))
            if j[0] == "Yo":
                interjection.append((i, cont))
            if j == "SP":
                preposition.append((i, cont))

            if j == "Fc":
                comas.append((j, cont))
            if j == "Fp":
                if cont_negative > 1:
                    doble_negacion += 1
                    doble_negacion_array.append(negative_text)
                cont_negative = 0
                negative_text = ""
                puntos.append(j)
            if j == "Fx":
                punto_coma.append((j, cont))

            if j[0] == "F":
                puntuacion.append((j, cont))

            if j[0] != "F" and i not in frecuencia:
                frecuencia.append(i)

            if i.lower() in dic_frecuencia_sub:
                if dic_frecuencia_sub[i.lower()] >= 108:
                    muy_frecuentes_sub.append((i.lower(), cont))
                if 108 > dic_frecuencia_sub[i.lower()] > 31:
                    frecuentes_sub.append((i.lower(), cont))
                if dic_frecuencia_sub[i.lower()] <= 31:
                    poco_frecuentes_sub.append((i.lower(), cont))

            cont += 1

        muy_frecuentes = []
        frecuentes = []
        poco_frecuentes = []

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
                    if 4 > dic_frecuencia[p.lower()] > 0.3:
                        frecuentes.append((p.lower(), cont2))
                        valor = "es frecuente"
                    if dic_frecuencia[p.lower()] <= 0.3:
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

        N_sentences = len(frases)
        Comas = (len(comas)) / len(frases)
        Participle_Verbs_number = (len(verbp) * 100) / lenwords
        Por_Abreviaturas = (len(abrv) * 100) / lenwords
        Ratio_Caracteres_Palabra = caracteres / lenwords
        Por_Simbolos = (len(errores) * 100) / lenwords
        Preposition_number = (len(preposition) * 100) / lenwords
        Infinitive_Verbs_number = (len(verbi) * 100) / lenwords
        Determiners_number = (len(determiner) * 100) / lenwords
        Por_Sinonimos = (len(sinonimos) * 100) / lenwords
        Por_comillas = (len(comillas) * 100) / lenwords
        Por_verbs = (len(verbs) * 100) / lenwords
        N_puntos = (len(puntos)) / len(frases)
        Por_siglas = (len(siglas) * 100) / lenwords
        Por_verbsg = (len(verbg) * 100) / lenwords
        Por_desc = (len(desconocidas) * 100) / lenwords
        Por_large = (len(large) * 100) / lenwords
        Por_superlative = (len(superlative) * 100) / lenwords
        Por_adverbs = (len(adverb) * 100) / lenwords
        Por_indeterminate = (len(indeterminate) * 100) / lenwords
        Por_numeros = (len(numeros) * 100) / lenwords
        Por_complex = (len(con_complex) * 100) / lenwords
        Por_m_frec = (len(muy_frecuentes) * 100) / len(words)
        Por_frec = (len(frecuentes) * 100) / len(words)
        Por_poco_frec = (len(poco_frecuentes) * 100) / len(words)
        P_F = lenwords / len(frases)
        L_P = caracteres / lenwords
        Por_puntos = (len(puntos) * 100) / lenwords
        Por_puntos_coma = (len(punto_coma) * 100) / lenwords
        Por_fechas = (len(date) * 100) / lenwords
        Por_dn = (doble_negacion * 100) / lenwords
        Por_partitivos = (len(partitivos) * 100) / lenwords
        Por_presente_indicativo = (len(presente_indicativo) * 100) / lenwords
        Por_subjuntivo = (len(subjuntivo) * 100) / lenwords
        Por_condicional = (len(condicional) * 100) / lenwords
        Por_nverbs = (nverbseguidos * 100) / lenwords
        por_comas = (len(comas) * 100) / lenwords
        por_noun = (len(noun) * 100) / lenwords
        por_largas = (len(large) * 100) / lenwords
        por_muy_frecuentes_sub = (len(muy_frecuentes_sub) * 100) / lenwords
        documento = "vacio"

        dic_resultados = {}

        if Por_presente_indicativo <= 3.058824:
            resultados.append(("indicativo", Por_presente_indicativo))
            dic_resultados["indicativo"] = verbos_no_indicativo
            if Por_comillas <= 0.280767:
                resultados.append(("comillas", Por_comillas))
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
            if Por_comillas > 0.280767:
                    resultados.append(("comillas", Por_comillas))
                    documento = "Dificil"
        if Por_presente_indicativo > 3.058824:
            dic_resultados["indicativo"] = verbos_no_indicativo
            resultados.append(("indicativo", Por_presente_indicativo))
            if len(words) <= 489:
                resultados.append(("palabras", len(words)))
                if por_comas <= 6.621773:
                    resultados.append(("comas", por_comas))
                    dic_resultados["comas"] = comas
                    if len(words) <= 306:
                        documento = "Dificil"
                    if len(words) > 306:
                        if Participle_Verbs_number <= 0.974026:
                            dic_resultados["participio"] = verbp
                            resultados.append(("participio", Participle_Verbs_number))
                            documento = "Facil"
                        if Participle_Verbs_number > 0.974026:
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
                        if Preposition_number <= 14.554637:
                            dic_resultados["preposiciones"] = preposition
                            resultados.append(("preposiciones", Preposition_number))
                            documento = "Facil"
                        if Preposition_number > 14.554637:
                            resultados.append(("preposiciones", Preposition_number))
                            dic_resultados["preposiciones"] = preposition
                            if Por_comillas <= 0.214823:
                                dic_resultados["comillas"] = comillas
                                resultados.append(("comillas", Por_comillas))
                                if Por_frec <= 3.342618:
                                    dic_resultados["frecuentes"] = frecuentes
                                    resultados.append(("frecuentes", Por_frec))
                                    documento = "Facil"
                                if Por_frec > 3.342618:
                                    resultados.append(("frecuentes", Por_frec))
                                    dic_resultados["frecuentes"] = frecuentes
                                    documento = "Dificil"
                            if Por_comillas > 0.214823:
                                resultados.append(("comillas", Por_comillas))
                                documento = "Dificil"
                    if por_muy_frecuentes_sub > 68.782161:
                        dic_resultados["muy_frecuente_sub"] = muy_frecuentes_sub
                        resultados.append(("muy_frecuente_sub", por_muy_frecuentes_sub))
                        documento = "Facil"
                if por_largas > 7.234043:
                    dic_resultados["largas"] = large
                    resultados.append(("largas", por_largas))
                    if Por_presente_indicativo <= 4.41989:
                        resultados.append(("indicativo", Por_presente_indicativo))
                        documento = "Dificil"
                        dic_resultados["indicativo"] = verbos_no_indicativo
                    if Por_presente_indicativo > 4.41989:
                        resultados.append(("indicativo", Por_presente_indicativo))
                        documento = "Facil"
                        dic_resultados["indicativo"] = verbos_no_indicativo

        resultados[0] = ("Resumen", documento)

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
            "Percentage_desconocidas": (len(desconocidas) * 100) / lenwords,
            "Resumen": documento,
            "Analisis_Reglas": resultados
        })

        print("Fin\n")
        return resultados, fjson, self.title, self.text, dic_resultados, analisis
