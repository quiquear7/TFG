#! /usr/bin/python3

import pyfreeling
import sys


def ProcessSentences(ls):
    # for each sentence in list
    for s in ls:
        # for each word in sentence
        for w in s:
            # print word form
            print("word '" + w.get_form() + "'")
            # print possible analysis in word, output lemma and tag
            print(" Possible analysis: {", end="")
            for a in w:
                print(" (" + a.get_lemma() + "," + a.get_tag() + ")", end="")
                print(" }")
                # print analysis selected by the tagger
                print(" Selected Analysis: (" + w.get_lemma() + "," + w.get_tag() + ")")
                # sentence separator
                print("")
