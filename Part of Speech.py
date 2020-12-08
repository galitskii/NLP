
# coding: utf-8
# функция prt_spch() принимает на вход слово, 
# а возвращает множество, в котором указано:
# NOUN - если слово может быть сущ., NPRO - если оно м. б. местоимением,
# VERB - если слово м.б. глаголом, OTHER - если ничего из перечисленного

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def prt_spch(word):
    p = morph.parse(word)
    l = []
    for i in range(len(p)):
        if p[i].tag.POS == 'NOUN':
            l.append('NOUN')
        if p[i].tag.POS == 'INFN' or p[i].tag.POS == 'VERB':
            l.append('VERB')
        if p[i].tag.POS == 'NPRO':
            l.append('NPRO')
    if len(l) == 0:
        return ('OTHER')
    return set(l)