import codecs
import os
import pickle
import sys
import nltk
from freeling import pyfreeling


def diccionario_frecuencia():
    dic_frecuencias = {}
    archivo_frecuencia = codecs.open("diccionarios/CREA_total.txt", "r", encoding="latin-1")
    for entrada in archivo_frecuencia:
        entrada = entrada.split()
        word = entrada[1]
        dic_frecuencias[word] = float(entrada[3])
    return dic_frecuencias


def diccionario_frecuencia_sub():
    '''dic_frecuencias = {}
    archivo_frecuencia = codecs.open("diccionarios/es_full.txt", "r", encoding="latin-1")
    for entrada in archivo_frecuencia:
        entrada = entrada.split()
        word = entrada[0]
        dic_frecuencias[word] = int(entrada[1])
    return dic_frecuencias'''


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


def printTree(ptree, depth):
    node = ptree.begin()

    print(''.rjust(depth * 2), end='')
    info = node.get_info()
    if info.is_head():
        print('+', end='')

    nch = node.num_children()
    if nch == 0:
        w = info.get_word()
        print('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()), end='')

    else:
        print('{0}_['.format(info.get_label()))

        for i in range(nch):
            child = node.nth_child_ref(i)
            printTree(child, depth + 1)

        print(''.rjust(depth * 2), end='')
        print(']', end='')

    print('')


def printDepTree(dtree, depth):
    node = dtree.begin()

    print(''.rjust(depth * 2), end='')

    info = node.get_info()
    link = info.get_link()
    linfo = link.get_info()
    print('{0}/{1}/'.format(link.get_info().get_label(), info.get_label()), end='')

    w = node.get_info().get_word()
    print('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()), end='')

    nch = node.num_children()
    if nch > 0:
        print(' [')

        for i in range(nch):
            d = node.nth_child_ref(i)
            if not d.begin().get_info().is_chunk():
                printDepTree(d, depth + 1)

        ch = {}
        for i in range(nch):
            d = node.nth_child_ref(i)
            if d.begin().get_info().is_chunk():
                ch[d.begin().get_info().get_chunk_ord()] = d

        for i in sorted(ch.keys()):
            printDepTree(ch[i], depth + 1)

        print(''.rjust(depth * 2), end='')
        print(']', end='')

    print('')


def freeling(text):
    if "FREELINGDIR" not in os.environ:
        if sys.platform == "win32" or sys.platform == "win64":
            os.environ["FREELINGDIR"] = "C:\\Program Files"
        else:
            os.environ["FREELINGDIR"] = "/usr/local"
        print("FREELINGDIR environment variable not defined, trying ", os.environ["FREELINGDIR"], file=sys.stderr)

    if not os.path.exists(os.environ["FREELINGDIR"] + "/share/freeling"):
        print("Folder", os.environ["FREELINGDIR"] + "/share/freeling",
              "not found.\nPlease set FREELINGDIR environment variable to FreeLing installation directory",
              file=sys.stderr)
        sys.exit(1)

    # Location of FreeLing configuration files.
    DATA = os.environ["FREELINGDIR"] + "/share/freeling/"

    # Init locales
    pyfreeling.util_init_locale("default")

    # create language detector. Used just to show it. Results are printed
    # but ignored (after, it is assumed language is LANG)
    la = pyfreeling.lang_ident(DATA + "common/lang_ident/ident-few.dat");

    # create options set for maco analyzer. Default values are Ok, except for data files.
    LANG = "es"
    op = pyfreeling.maco_options(LANG)
    op.set_data_files("",
                      DATA + "common/punct.dat",
                      DATA + LANG + "/dicc.src",
                      DATA + LANG + "/afixos.dat",
                      "",
                      DATA + LANG + "/locucions.dat",
                      DATA + LANG + "/np.dat",
                      DATA + LANG + "/quantities.dat",
                      DATA + LANG + "/probabilitats.dat")

    # create analyzers
    tk = pyfreeling.tokenizer(DATA + LANG + "/tokenizer.dat")
    sp = pyfreeling.splitter(DATA + LANG + "/splitter.dat")
    sid = sp.open_session()
    mf = pyfreeling.maco(op)

    # activate mmorpho odules to be used in next call
    mf.set_active_options(False, True, True, True,  # select which among created
                          True, True, False, True,  # submodules are to be used.
                          True, True, True, True)  # default: all created submodules are used

    # create tagger, sense anotator, and parsers
    tg = pyfreeling.hmm_tagger(DATA + LANG + "/tagger.dat", True, 2)
    sen = pyfreeling.senses(DATA + LANG + "/senses.dat")
    parser = pyfreeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
    dep = pyfreeling.dep_txala(DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())

    # process input text
    lin = text
    print("Text language is: " + la.identify_language(lin))

    l = tk.tokenize(lin)
    ls = sp.split(sid, l, False)

    ls = mf.analyze(ls)
    ls = tg.analyze(ls)
    ls = sen.analyze(ls)
    ls = parser.analyze(ls)
    ls = dep.analyze(ls)
    analisis = []
    words = 0

    ## output results
    for s in ls:
        ws = s.get_words()
        words += len(ws)
        for w in ws:
            analisis.append((w.get_form(), w.get_tag(), w.get_lemma()))

    # clean up
    sp.close_session(sid)
    return analisis, words
