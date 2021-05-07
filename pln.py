import codecs
import pickle
import string
import nltk
import nltk.data
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
                if i == "." and words[cont + 1].istitle() is False and words[cont + 1].isdigit() is False:
                    title.append((words[cont + 1], cont))'''
            if i == "cosa" or i == "algo" or i == "asunto":
                indeterminate.append((i, cont))
            if ("º" in i or "ª" in i) or (j[0] == "M" and j[1] == "O"):
                numbers.append((i, cont))
            if '"' == i or i == "'":
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
                        if t in sinonimos_usados:
                            usado = 1
                            sinonimos_usados[t] += i + ", "
                            sinonimos.append((i, cont))
                    if usado == 0:
                        sinonimos_usados[k] = ""
            else:
                sinonimos_usados[k] = ""

            if j == "Fc":
                comas.append(cont)
            if j == "Fp":
                puntos.append(cont)
            if j == "Fx":
                punto_coma.append(cont)

            existe = 1
            if "_" in i:
                z = i.split("_")
                for t in z:
                    if t not in dic_frecuencia:
                        existe = 0
                    if t in dic_abreviaturas:
                        abrv.append((i, cont))
                    if t in dic_siglas:
                        siglas.append((i, cont))

            if (dic_frecuencia.get(i.lower())) or ("_" in i and existe == 1) or j[0] == "F":
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
                if j[0] == "V":
                    verbs.append((i, cont))
                    if j[2] == "N":
                        verbi.append((i, cont))
                    if j[2] == "G":
                        verbg.append((i, cont))
                    if j[2] == "P":
                        verbp.append((i, cont))
                if j[0] == "Z":
                    number.append((i, cont))
                if j[0] == "W":
                    date.append((i, cont))
                if j[0] == "Yo":
                    interjection.append((i, cont))
                if j == "SP":
                    preposition.append((i, cont))
            else:
                desconocidas.append((i, cont))

            cont += 1

        muy_frecuentes = []
        frecuentes = []
        poco_frecuentes = []

        sentence = 1
        fjson["Sentences_Set"] = []
        for i in frases:
            wordsjson = []
            words_temp = word_tokenize(i, "spanish")
            for p in words_temp:
                if p.lower() in dic_frecuencia:
                    valor = ""
                    if dic_frecuencia[p.lower()] >= 1:
                        muy_frecuentes.append((p.lower(), cont))
                        valor = "es muy frecuente"
                    if 1 > dic_frecuencia[p.lower()] > 0.3:
                        frecuentes.append((p.lower(), cont))
                        valor = "es frecuente"
                    if dic_frecuencia[p.lower()] <= 0.3:
                        poco_frecuentes.append((p.lower(), cont))
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
        documento = "vacio"

        if N_sentences <= 24:
            resultados.append(("N_sentences", N_sentences))
            if Comas <= 0.6:
                resultados.append(("Comas", Comas))
                documento = "Dificil"
            if Comas > 0.6:
                resultados.append(("Comas", Comas))
                if N_sentences <= 5:
                    documento = "Dificil"
                if N_sentences > 5:
                    if Participle_Verbs_number <= 1.183432:
                        resultados.append(("Participle_Verbs_number", Participle_Verbs_number, verbp))
                        if Por_Abreviaturas <= 2.287582:
                            resultados.append(("Por_Abreviaturas", Por_Abreviaturas, abrv))
                            documento = "Facil"
                        if Por_Abreviaturas > 2.287582:
                            resultados.append(("Por_Abreviaturas", Por_Abreviaturas, abrv))
                            documento = "Dificil"
                    if Participle_Verbs_number > 1.183432:
                        resultados.append(("Participle_Verbs_number", Participle_Verbs_number, verbp))
                        if Ratio_Caracteres_Palabra <= 4.760141:
                            resultados.append(("Ratio_Caracteres_Palabra", Ratio_Caracteres_Palabra))
                            if Por_Simbolos <= 0.93633:
                                resultados.append(("Por_Simbolos", Por_Simbolos, errores))
                                documento = "Dificil"
                            if Por_Simbolos > 0.93633:
                                resultados.append(("Por_Simbolos", Por_Simbolos, errores))
                                documento = "Facil"
                        if Ratio_Caracteres_Palabra > 4.760141:
                            resultados.append(("Ratio_Caracteres_Palabra", Ratio_Caracteres_Palabra))
                            if Participle_Verbs_number <= 2.754237:
                                if Participle_Verbs_number <= 1.731602:
                                    documento = "Dificil"
                                if Participle_Verbs_number > 1.731602:
                                    if Preposition_number <= 14.814815:
                                        resultados.append(("Preposition_number", Preposition_number, preposition))
                                        documento = "Facil"
                                    if Preposition_number > 14.814815:
                                        resultados.append(("Preposition_number", Preposition_number))
                                        if Infinitive_Verbs_number <= 4.850746:
                                            resultados.append(("Infinitive_Verbs_number", Infinitive_Verbs_number, verbi))
                                            if Determiners_number <= 12.418906:
                                                resultados.append(("Determiners_number", Determiners_number, determiner))
                                                if Por_Sinonimos <= 2.517623:
                                                    resultados.append(("Por_Sinonimos", Por_Sinonimos, sinonimos_usados))
                                                    documento = "Facil"
                                                if Por_Sinonimos > 2.517623:
                                                    resultados.append(("Por_Sinonimos", Por_Sinonimos, sinonimos_usados))
                                                    documento = "Dificil"
                                            if Determiners_number > 12.418906:
                                                resultados.append(("Determiners_number", Determiners_number, determiner))
                                                documento = "Dificil"
                                        if Infinitive_Verbs_number > 4.850746:
                                            resultados.append(("Infinitive_Verbs_number", Infinitive_Verbs_number, verbi))
                                            documento = "Facil"
                                if Participle_Verbs_number > 2.754237:
                                    documento = "Dificil"
        if N_sentences > 24:
            resultados.append(("N_sentences", N_sentences))
            if Por_comillas <= 0:
                resultados.append(("Por_comillas", Por_comillas, comillas))
                if Por_verbs <= 9.968354:
                    resultados.append(("Por_verbs", Por_verbs, verbs))
                    if N_puntos <= 0.942857:
                        resultados.append(("N_puntos", N_puntos))
                        documento = "Facil"
                    if N_puntos > 0.942857:
                        resultados.append(("N_puntos", N_puntos))
                        documento = "Dificil"
                if Por_verbs > 9.968354:
                    resultados.append(("Por_verbs", Por_verbs, verbs))
                    documento = "Facil"
            if Por_comillas > 0:
                resultados.append(("Por_comillas", Por_comillas, comillas))
                documento = "Dificil"

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
            "Resumen": documento
        })

        # collection.insert_one(fjson)
        # client.close()

        print("Fin\n")
        return resultados, fjson, self.title, self.text
