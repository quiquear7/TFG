import codecs
import pickle
import nltk
import nltk.data

'''import time
import requests
from bs4 import BeautifulSoup
'''
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

    def __init__(self, text, directory):
        self.text = text
        self.directory = directory

    def process(self):

        fjson = {
            "Title": "texto.txt",
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
        print(frases2)
        words = word_tokenize(self.text, "spanish")
        print(words)

        freq = nltk.FreqDist(words)
        print("freq")
        print(freq.items())

        clean = frases[:]
        sr = stopwords.words('spanish')
        for token in frases:
            if token in sr:
                clean.remove(token)
        print("\n")
        print("Texto limpio \n")

        palabras = []
        dic = codecs.open("diccionarios/0_palabras_todas.txt", "r", encoding="utf-8")
        for i in dic:
            palabras.append(i.rstrip())

        frecuencia = {}
        archivo_frecuencia = codecs.open("diccionarios/CREA_total.TXT", "r", encoding="latin-1")
        for entrada in archivo_frecuencia:
            entrada = entrada.split()
            if len(entrada) >= 4:
                word = entrada[1]
                frequ = entrada[3]
                frecuencia[word] = float(frequ)

        sin = codecs.open("diccionarios/sinonimos_final.txt", "r", encoding="utf-8")
        dic_sin = {}
        for entrada in sin:
            pal = entrada.split(", ")
            dic_sin[pal[0]] = pal

        abrv = codecs.open("diccionarios/abreviaturas.txt", "r", encoding="utf-8")
        dic_abreviaturas = {}
        for entrada in abrv:
            pal = entrada.split(":")
            dic_abreviaturas[pal[0]] = pal[1]

        sigl = codecs.open("diccionarios/siglas-final.txt", "r", encoding="utf-8")
        dic_siglas = {}
        for entrada in sigl:
            pal = entrada.split(":")
            dic_siglas[pal[0]] = pal[1]

        hom = codecs.open("diccionarios/homonimas.txt", "r", encoding="utf-8")
        dic_hom = {}
        for entrada in hom:
            pal = entrada.split()
            print(pal)
            dic_hom[pal[0]] = pal[1]

        for i in words:
            synonyms = []
            for syn in wordnet.synsets(i):
                for lemma in syn.lemmas(lang="spa"):
                    synonyms.append(lemma.name())
            print(i)
            print(synonyms)
            print("\n")

        print("sigla")

        sigla = []
        f = codecs.open('diccionarios/siglas-final.txt', "a", "utf-8")
        for i in freq.items():
            if i[0].isupper() and int(i[1]) > 1 and 2 <= len(i[0]) <= 5:
                if i[0] not in dic_abreviaturas:
                    f.write(i[0]+'\n')
                    sigla.append(i[0])
        f.close()
        print(sigla)

        spanish_stemmer = SnowballStemmer('spanish')

        for i in words:
            print(i)
            print(spanish_stemmer.stem(i), end='\n')
            print("\n")

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
        cont = 0
        for i in words:
            if i.isupper():
                upper.append(i)
            if i == ";" or i == "&" or i == "%" or i == "/" or i == "(" or i == ")" or i == "^" or i == "[" or i == "]" or i == "{" or i == "}" or i == "etc." or i == "...":
                errores.append((i, cont))
            if len(i) > 15:
                large.append((i, cont))
            if "ísimo" in i:
                superlative.append((i, cont))
            if "mente" in i:
                adverbs.append((i, cont))
            if "@" in i:
                arroba.append((i, cont))
            if cont < len(words) - 1:
                if i == "." and words[cont + 1].istitle() is False and words[cont + 1].isdigit() is False:
                    title.append((words[cont + 1], cont))
            if i == "cosa" or i == "algo" or i == "asunto":
                indeterminate.append((i, cont))
            if "º" in i or "ª" in i:
                numbers.append((i, cont))
            try:
                datetime.strptime(i, '%YYYY-%m-%d')
                date.append((i, cont))
            except ValueError:
                try:
                    datetime.strptime(i, '%d-%m-%YYYY')
                    date.append((i, cont))
                except ValueError:
                    try:
                        datetime.strptime(i, '%YYYY/%m/%d')
                        date.append((i, cont))
                    except ValueError:
                        try:
                            datetime.strptime(i, '%d/%m/%YYYY')
                            date.append((i, cont))
                        except ValueError:
                            print("no es una fecha")
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
                if p.lower() in frecuencia:
                    valor = ""
                    if frecuencia[p.lower()] >= 0.3:
                        valor = "es muy frecuente"
                    if 0.3 > frecuencia[p.lower()] > 0.1:
                        valor = "es frecuente"
                    if frecuencia[p.lower()] <= 0.1:
                        valor = "es poco frecuente"
                    wordsjson.append({
                        "Word": p + "",
                        "Frequency_value": frecuencia[p.lower()],
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

        diccionario = {}
        archivo_diccionario = codecs.open("diccionarios/diccionario-freeling-spa.txt", "r", encoding="utf-8")

        for entrada in archivo_diccionario:
            entrada = entrada.rstrip()
            camps = entrada.split(":")
            if len(camps) >= 3:
                forma = camps[0]
                lema = camps[1]
                etiqueta = camps[2]
                if forma in diccionario:
                    diccionario[forma] = diccionario.get(forma, "") + " " + lema + " " + etiqueta
                else:
                    diccionario[forma] = lema + " " + etiqueta

        # Añadimos los signos de puntuación
        diccionario['"'] = '" Fe'
        diccionario["'"] = "' Fe"
        diccionario['.'] = '. Fp'
        diccionario[','] = ', Fc'
        diccionario[';'] = '; Fx'
        diccionario[':'] = ': Fd'
        diccionario['('] = '( Fpa'
        diccionario[')'] = ') Fpt'
        diccionario['['] = '[ Fca'
        diccionario[']'] = '] Fct'

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
        for forma in words:
            if forma.lower() in palabras:
                if forma.lower() in diccionario:
                    info = diccionario[forma.lower()]
                    print(info)
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
                    if et[1][0] == "Z":
                        number.append(et[0])
                    if et[1][0] == "S":
                        preposition.append(et[0])
                else:
                    info = "DESCONOCIDA"
                print(forma + " " + info)
            else:
                desconocidas.append(forma)

            print("\n")

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
        # print(desconocidas)

        '''for i in words:
            print(i, end="\n")
            url = "https://www.wordreference.com/sinonimos/" + i.lower()
            page = requests.get(url)
            html = BeautifulSoup(page.content, 'html.parser')
            div = html.find(class_='trans clickable')
            if div is not None:
                titulo = div.find_next('h3').text.strip()
                if titulo in i.lower():
                    sinonimos = div.find_next('ul').text.strip()
                    print(i, " ", sinonimos)
            print("\n")'''

        sinonimos_usados = {}
        for i in words:
            i = i.lower()
            if i not in sinonimos_usados:
                if i in dic_sin:
                    x = dic_sin[i]
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
        # print(sinonimos_usados)

        n_sin = 0
        for i in sinonimos_usados.values():
            if i != "":
                n_sin += 1
        # print(n_sin)

        # Etiquetado
        print("Etiquetado")

        '''entrada = codecs.open("diccionarios/wikicorpus3.txt", "r", encoding="utf-8")

        tagged_words = []
        tagged_sents = []
        tagged_sents_per_unigrams = []
        for linia in entrada:
            linia = linia.rstrip()
            if linia.startswith("<") or len(linia) == 0:
                # nova linia
                if len(tagged_words) > 0:
                    tagged_sents.append(tagged_words)
                    tagged_sents_per_unigrams.append(tagged_words)
                    tagged_words = []
            else:
                camps = linia.split(" ")
                forma = camps[0]
                lema = camps[1]
                etiqueta = camps[2]
                tupla = (forma, etiqueta)
                tagged_words.append(tupla)

        if len(tagged_words) > 0:
            tagged_sents.append(tagged_words)
            tagged_sents_per_unigrams.append(tagged_words)
            tagged_words = []

        diccionario = codecs.open("diccionarios/diccionario-freeling-spa.txt", "r", encoding="utf-8")

        for linia in diccionario:
            linia = linia.rstrip()
            camps = linia.split(":")
            if len(camps) >= 3:
                forma = camps[0]
                lema = camps[1]
                etiqueta = camps[2]
                tupla = (forma, etiqueta)
                tagged_words.append(tupla)
        tagged_sents_per_unigrams.append(tagged_words)

        default_tagger = nltk.DefaultTagger("NP00000")
        affix_tagger = nltk.AffixTagger(tagged_sents_per_unigrams, affix_length=-3, min_stem_length=2,
                                        backoff=default_tagger)
        unigram_tagger_diccionari = nltk.UnigramTagger(tagged_sents_per_unigrams, backoff=affix_tagger)
        unigram_tagger = nltk.UnigramTagger(tagged_sents, backoff=unigram_tagger_diccionari)
        bigram_tagger = nltk.BigramTagger(tagged_sents, backoff=unigram_tagger)
        trigram_tagger = nltk.TrigramTagger(tagged_sents, backoff=bigram_tagger)

        sortida = open('etiq-spanish.pkl', 'wb')
        pickle.dump(trigram_tagger, sortida, -1)
        sortida.close()'''

        '''entrada = open('etiquetador-spa.pkl', 'rb')
        etiquetador = pickle.load(entrada)
        entrada.close()
        analisis = etiquetador.tag(words)
        print(analisis)'''

        '''dabreviaturas = codecs.open("diccionarios/abreviatures.txt", "r", encoding="utf-8")
        abreviaturas = {}
        for i in dabreviaturas:
            i=i.rstrip()
            abreviaturas[i]=i
        print(abreviaturas)
        abrv=[]
        for i in words:
            i = i.rstrip()
            i = i.rstrip(".")
            if i in abreviaturas:
                print(i)
                abrv.append(i)
        print(abrv)
        print((len(abrv) * 100) / len(words))'''
        abrv = []
        siglas = []
        homo = []
        for i in words:
            if i in dic_abreviaturas:
                abrv.append(i)
            if i in dic_siglas:
                siglas.append(i)
            if i in dic_hom:
                homo.append(i)
        print(abrv)
        print((len(abrv) * 100) / len(words))
        print(siglas)
        print((len(siglas) * 100) / len(words))
        print(homo)
        print((len(homo) * 100) / len(words))

        with open(self.directory + '/data.json', 'w') as file:
            json.dump(fjson, file, ensure_ascii=False, indent=4)

        print("THE END")
