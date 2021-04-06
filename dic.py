import codecs
import pickle

import nltk


def diccionario_frecuencia():
    dic_frecuencias = {}
    archivo_frecuencia = codecs.open("diccionarios/CREA_total.TXT", "r", encoding="latin-1")
    for entrada in archivo_frecuencia:
        entrada = entrada.split()
        if len(entrada) >= 4:
            word = entrada[1]
            frequ = entrada[3]
            dic_frecuencias[word] = float(frequ)
    return dic_frecuencias


def diccionario_sinonimos():
    dic_sinonimos = {}
    sin = codecs.open("diccionarios/sinonimos_final.txt", "r", encoding="utf-8")
    for entrada in sin:
        pal = entrada.split(", ")
        dic_sinonimos[pal[0]] = pal
    return dic_sinonimos


def diccionario_abreviaturas():
    dic_abreviaturas = {}
    abrv = codecs.open("diccionarios/abreviaturas.txt", "r", encoding="utf-8")
    for entrada in abrv:
        pal = entrada.split(":")
        dic_abreviaturas[pal[0]] = pal[1]
    dabreviaturas = codecs.open("diccionarios/abreviatures.txt", "r", encoding="utf-8")
    for i in dabreviaturas:
        i = i.rstrip()
        dic_abreviaturas[i] = i
    return dic_abreviaturas


def diccionario_siglas():
    dic_siglas = {}
    sigl = codecs.open("diccionarios/siglas-final.txt", "r", encoding="utf-8")
    for entrada in sigl:
        pal = entrada.split(":")
        dic_siglas[pal[0]] = pal[1]
    return dic_siglas


def diccionario_homonimas():
    dic_hom = {}
    hom = codecs.open("diccionarios/homonimas.txt", "r", encoding="utf-8")
    for entrada in hom:
        pal = entrada.split()
        dic_hom[pal[0]] = pal[1]
    return dic_hom


def diccionario_palabras():
    palabras = []
    dic = codecs.open("diccionarios/0_palabras_todas.txt", "r", encoding="utf-8")
    for i in dic:
        palabras.append(i.rstrip())
    return palabras


def diccionario_freeling():
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
    return diccionario


def etiquetado():
    diccionario = diccionario_freeling()
    entrada = codecs.open("diccionarios/fragmento-wikicorpus-tagged-spa.txt", "r", encoding="utf-8")

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
    sortida.close()
