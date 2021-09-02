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
import csv


class EntrenarCsv:

    def __init__(self, text, directory, title, tipo):
        self.text = text  # texto que se va a analizar
        self.directory = directory  # directorio donde se va a almacenar el archivo csv
        self.title = title  # titulo del archivo a analizar
        self.tipo = tipo  # guarda si el archivo es facil o dificil

    def process(self):

        """obtenemos listado con las frases tokenizadas"""
        frases = sent_tokenize(self.text, "spanish")

        """obtenemos listado con las palabras tokenizadas"""
        words = word_tokenize(self.text, "spanish")

        """obtenemos una lista de tuplas con las frecuencias de las palabras"""
        freq = nltk.FreqDist(words)


        punct = string.punctuation  # lista con los signos de

        '''creamos una lista de tuplas con la palabra y su frecuencia'''
        freq2 = []
        for i in freq:
            if i not in punct:  # comprobamos que no la palabra no sea un signo de puntuación
                freq2.append((i, freq[i]))

        """calculamos cuantas palabras son específicas y generales"""
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

        '''calculamos los caracteres totales de las palabras'''
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

        '''analisis nos devuelve una lista con el etiquetado de las palabras, en lenwords se alamacena el número de 
                palabras etiquetadas'''
        analisis, lenwords = dic.freeling(self.text)  # obtenemos el etiquetado y el número de palabras
        if lenwords == 0:  # si el etiquetado falla utilizamos otro etiquetado
            entrada = open('diccionarios/etiquetador-spa.pkl', 'rb')
            etiquetador = pickle.load(entrada)
            analisis = etiquetador.tag(words)
            lenwords = len(words)
            entrada.close()

        etc = []  # almacena la abreviatura 'etc'
        abrv = []  # almacena las abrevituras en el texto
        siglas = []  # almacena las siglas del texto
        homo = []  # almacena los homonimos del texto
        sinonimos_usados = {}  # almacena los sinonimos del texto
        numeros = []  # almacena los números del texto
        errores = []  # almacena las simbolos del texto
        large = []  # almacena las palabras largas del texto
        superlative = []  # almacena los superlativos del texto
        adverbs = []  # almacena los adverbios del texto
        indeterminate = []  # almacena los indeterminados
        numbers = []  # almacena los numeros del texto
        comillas = []  # almacena las comillas del texto
        con_complex = []  # almacena los conectores complejos
        presente_indicativo = []  # almacena los verbos en presente de indicativo
        subjuntivo = []  # almacena verbos en subjuntivo
        condicional = []  # almacena verbos condicionales
        adjective = []  # almacena adejetivos
        conjunction = []  # almacena conjunciones
        determiner = []  # almacena determinantes
        noun = []  # almacena sustantivos
        pronoun = []  # almacena pronombres
        adverb = []  # almacena adverbios
        preposition = []  # almacena preposiciones
        verbs = []  # almacena verbos
        verbi = []  # almacena verbos en infinitivo
        verbg = []  # almacena verbos en gerundio
        verbp = []  # almacena verbos en participio
        imperative = []  # almacena verbos en imperativo
        number = []  # almacena numeros
        date = []  # almacena fechas
        interjection = []  # almacena interjecciones
        desconocidas = []  # almacena palabras desconocidas
        sinonimos = []  # almacena sinonimos
        nverbseguidos = 0  #  almacena cuantos verbos seguidos existen
        puntos = []  # almacena el número de puntos en el texto
        comas = []  # almacena las comas del texto
        punto_coma = []  # almacena los punto y comas del texto
        doble_negacion = 0  # almacena el número de dobles negaciones en el texto
        verbos_seguidos = []  # almacena los verbos que estan seguidos
        partitivos = []  # almacena los partitivos del texto
        sin = []  # almacena los sinonimos sin repetición
        cont = 0  # contador para obtener la posición de la palabra en el texto
        cont_negative = 0  # almacenas cuantas negaciones hay en una frase
        negative_text = ""  # obtiene las cadenas de las negaciones de una frase
        doble_negacion_array = []  # almacena las cadenas de las dobles negaciones en un array
        puntuacion = []  # almacenas los signos de puntación en el texto

        """almacena las palabras muy frecuentes, frecuentes y poco frecuentes en base a dos listados"""

        """listado de RAE"""
        muy_frecuentes = []
        frecuentes = []
        poco_frecuentes = []

        """Listado de Subtitulos"""
        muy_frecuentes_sub = []
        frecuentes_sub = []
        poco_frecuentes_sub = []

        mayus_no_sigla = []  # almacena las mmayusculas que no son siglas en el texto
        frecuencia = []  # almacena la frecuencia de las palabras en el texto
        ordinales = []  # almacena los número ordinales
        date_mal = []  # almacena las fechas que están con formato erroneo
        romanos = []  # almacena números romanos
        dos_puntos = []  # almacena las posiciones donde hay dos puntos en el texto
        otro_idioma = []  # almacena palabras que no estén en castellano
        proper_noun = []  # almacena nombres propios
        futuro = []  # almacena verbos en futuro
        pasado = []  # almacena verbos en pasado

        '''en este momento recorremos una a una cada palabra etiquetada'''
        for x in analisis:
            i = x[0]  # palabra a analizar
            j = x[1]  # etiqueta
            k = i
            if len(x) == 3:
                k = x[2]  # utilizamos la variable k para almacenar el lema en caso de que exista

            """comprueba si una palabra es de otro idioma y no es una sigla, abreviatura o signo de puntuación"""
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

            """calcula siglas que no esten guardadas en el listado de siglas, para ello comprueba si está en mayusuculas,
            no son una palabra y tienen entre 2 y 7, si no se cumple se asume que es una palabra en mayuscula, el listado
            de siglas se actualiza agregando la nueva palabra"""
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

            """busca los simbolos en el texto"""
            if "&" in i or "%" in i or "/" in i or "(" in i or ")" in i or "^" in i or "[" in i or "]" in i or "{" in i or "}" in i or "..." in i or "ª" in i:
                errores.append((i, cont))
            "etc"
            if "etc" in i:
                etc.append((i, cont))

            '''si la palabra tiene mas de 10 caracteres es considerada larga '''
            if len(i) > 10 and "_" not in i:
                large.append((i, cont))

            """Superlativos"""
            if j[0] == "A" and j[2] == "S":
                superlative.append((i, cont))

            """Adverbios"""
            if j[0] == "R" and "mente" in i:
                adverbs.append((i, cont))

            "Arroba"
            if "@" in i:
                errores.append((i, cont))

            """palabras inderterminadas como cosa, algo o asunto"""
            if i == "cosa" or i == "algo" or i == "asunto":
                indeterminate.append((i, cont))

            """Numeros"""
            if ("º" in i or "ª" in i) or (j[0] == "M" and j[1] == "O"):
                numbers.append((i, cont))

            """Comillas"""
            if '"' == i or "«" == i or "»" == i or "'" == i:
                comillas.append((i, cont))
            """Numeros"""
            if i.isdigit():
                numeros.append((i, cont))

            """Comprueba si existen los siguientes conectores complejos"""
            if i.lower() == "por_lo_tanto":
                con_complex.append((i, cont))
            if i.lower() == "no_obstante":
                con_complex.append((i, cont))
            if i.lower() == "por_consiguiente":
                con_complex.append((i, cont))
            if i.lower() == "sin" and analisis[cont + 1][0].lower() == "embargo":
                con_complex.append((i, cont))

            """Abreviaturas"""
            if i in dic_abreviaturas:
                abrv.append(i)

            """Siglas"""
            if i in dic_siglas:
                siglas.append(i)

            """Homonimas"""
            if i in dic_hom:
                homo.append(i)

            """Sinonimos"""
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

            """Abrebiatura y siglas"""
            if "_" in i:
                z = i.split("_")
                for t in z:
                    if t in dic_abreviaturas:
                        abrv.append(i)
                    if t in dic_siglas:
                        siglas.append(i)
            """Adejetivos"""
            if j[0] == "A":
                adjective.append(i)

            """Conjunciones"""
            if j[0] == "C":
                conjunction.append(i)

            """Determinantes"""
            if j[0] == "D":
                determiner.append(i)

            """Sustantivos"""
            if j[0] == "N":
                noun.append(i)
                """nombres propios"""
                if j[1] == "P":
                    proper_noun.append(i)

            """Pronombres"""
            if j[0] == "P":
                pronoun.append(i)

            """Adverbios"""
            if j[0] == "R":
                adverb.append(i)

                """Advebios de negación"""
                if j[1] == "N":
                    cont_negative += 1
                    negative_text += i + "-"


            if "ningun" in i or "ningún" in i:
                cont_negative += 1
                negative_text += i + "-"

            """Verbos """
            if j[0] == "V":
                verbs.append(i)

                """verbos consecutivos"""
                if analisis[cont + 1][1][0] == "V":
                    verbos_seguidos.append((i, analisis[cont + 1][0]))
                    nverbseguidos += 2

                """Infinitivo"""
                if j[2] == "N":
                    verbi.append(i)

                """Gerundio"""
                if j[2] == "G":
                    verbg.append(i)

                """Participio"""
                if j[2] == "P":
                    verbp.append(i)

                """Presente de Indicativo"""
                if j[2] == "I" and j[3] == "P":
                    presente_indicativo.append(i)

                """Subjuntivo"""
                if j[2] == "S":
                    subjuntivo.append(i)

                """Condicional"""
                if j[3] == "C":
                    condicional.append(i)

                """Futuro"""
                if j[3] == "F":
                    futuro.append(i)

                """Pasado"""
                if j[3] == "S":
                    pasado.append(i)

                """Imperativo"""
                if j[2] == "M":
                    imperative.append(i)

            """Numeros"""
            if j[0] == "Z":
                number.append(i)

                if len(j) > 1:
                    """Partitivos"""
                    if j[1] == "p" or j[1] == "d":
                        partitivos.append(i)

                """Ordinales"""
                if "º" in i:
                    ordinales.append((i, cont))

                """Fechas que no estan en el formato UNE"""
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

            """Fechas"""
            if j == "W":
                date.append(i)

                """fechas que no siguen la normativa UNE"""
                if "/" in i:
                    date_mal.append((i, cont))

                """Números romanos"""
                if "I" in i or "V" in i or "X" in i or "L" in i or "C" in i or "D" in i or "M" in i:
                    romanos.append((i, cont))

            """Interjecciones"""
            if j[0] == "Yo":
                interjection.append(i)

            """Proposiciones"""
            if j == "SP":
                preposition.append(i)

            """comas"""
            if j == "Fc":
                comas.append(j)

            """Puntos"""
            if j == "Fp":
                if cont_negative > 1:
                    doble_negacion += 1
                    doble_negacion_array.append(negative_text)
                cont_negative = 0
                negative_text = ""
                puntos.append(j)

            """Punto y coma"""
            if j == "Fx":
                punto_coma.append(j)

            """Cualquier signo de puntuación"""
            if j[0] == "F":
                puntuacion.append(j)

            """Frecuencia de una palabra"""
            if j[0] != "F" and i not in frecuencia:
                frecuencia.append(i)

            """Frecuenica según el listado de la RAE"""
            if i.lower() in dic_frecuencia:
                if dic_frecuencia[i.lower()] >= 4:
                    muy_frecuentes.append(i.lower())
                if 4 > dic_frecuencia[i.lower()] > 1:
                    frecuentes.append(i.lower())
                if dic_frecuencia[i.lower()] <= 1:
                    poco_frecuentes.append(i.lower())
            else:
                desconocidas.append(i.lower())

            """Frecuencia según el listado de subtitulos"""
            if i.lower() in dic_frecuencia_sub:
                if dic_frecuencia_sub[i.lower()] >= 108:
                    muy_frecuentes_sub.append(i.lower())
                if 108 > dic_frecuencia_sub[i.lower()] > 31:
                    frecuentes_sub.append(i.lower())
                if dic_frecuencia_sub[i.lower()] <= 31:
                    poco_frecuentes_sub.append(i.lower())

            cont += 1 # aumentamos el contador con la posición de la palabra

        """comprobamos si los resultados son iguales a 0 """
        if len(verbs) == 0:
            verbs.append("")
        if len(noun) == 0:
            noun.append("")

        """escribimos los porcentajes de las variables en el archivo CSV"""
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
