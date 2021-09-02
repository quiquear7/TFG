import codecs
import os
import pickle
import sys
import nltk
from freeling import pyfreeling

"""funcion para leer diccionario de frecuencias de la RAE"""
def diccionario_frecuencia():
    dic_frecuencias = {}
    archivo_frecuencia = codecs.open("diccionarios/CREA_total.txt", "r", encoding="latin-1")
    for entrada in archivo_frecuencia:
        entrada = entrada.split()
        word = entrada[1]
        dic_frecuencias[word] = float(entrada[3])
    return dic_frecuencias

"""funcion para leer diccionario de frecuencias de subtitulos"""
def diccionario_frecuencia_sub():
    dic_frecuencias = {}
    archivo_frecuencia = codecs.open("diccionarios/es_full.txt", "r", encoding="latin-1")
    for entrada in archivo_frecuencia:
        entrada = entrada.split()
        if len(entrada) == 2:
            word = entrada[0]
            dic_frecuencias[word] = int(entrada[1])
    return dic_frecuencias

"""funcion para leer diccionario de sinonimos"""
def diccionario_sinonimos():
    dic_sinonimos = {}
    sin = codecs.open("diccionarios/sinonimos_final.txt", "r", encoding="utf-8")
    for entrada in sin:
        pal = entrada.split(", ")
        dic_sinonimos[pal[0]] = pal
    return dic_sinonimos

"""funcion para leer diccionario de abreviaturas"""
def diccionario_abreviaturas():
    dic_abreviaturas = {}
    abrv = codecs.open("diccionarios/abreviaturas.txt", "r", encoding="utf-8")
    for entrada in abrv:
        pal = entrada.split(":")
        dic_abreviaturas[pal[0]] = pal[1].rstrip()
    dabreviaturas = codecs.open("diccionarios/abr-spa.txt", "r", encoding="utf-8")
    for i in dabreviaturas:
        i = i.rstrip()
        dic_abreviaturas[i] = i
    return dic_abreviaturas

"""funcion para leer diccionario de frecuencias de siglas"""
def diccionario_siglas():
    dic_siglas = {}
    sigl = codecs.open("diccionarios/siglas-final.txt", "r", encoding="utf-8")
    for entrada in sigl:
        pal = entrada.split(":")
        dic_siglas[pal[0]] = pal[1]
    return dic_siglas

"""funcion para leer diccionario de homonimos"""
def diccionario_homonimas():
    dic_hom = {}
    hom = codecs.open("diccionarios/homonimas.txt", "r", encoding="utf-8")
    for entrada in hom:
        pal = entrada.split()
        dic_hom[pal[0]] = pal[1].rstrip()
    return dic_hom

"""funcion para leer diccionario de freeling"""
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


"""función para realizar el etiquetado de FreeLing"""
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
    l = tk.tokenize(text)
    ls = sp.split(sid, l, True)

    ls = mf.analyze(ls)
    ls = tg.analyze(ls)
    ls = sen.analyze(ls)
    ls = parser.analyze(ls)
    ls = dep.analyze(ls)

    analisis = []
    words = 0
    cont = 0
    for s in ls:
        ws = s.get_words()
        words += len(ws) # obtenemos el número de palabras analizadas
        for w in ws:
            #guardamos la palabra, la etiqueta y el lema de cada palabra
            analisis.append((w.get_form(), w.get_tag(), w.get_lemma()))

        cont += 1

    sp.close_session(sid)
    return analisis, words
