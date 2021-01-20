'''
Кусок программы, которая позволит добавлять новые слова в базу.
Нужно ввести слово, получим часть данных о нём (не всё, поскольку 
не ясны все поля таблицы)
'''
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
def new_w(word):
    p = morph.parse(word)
    print(len(p))
    for i in range(len(p)):
        pos = p[i].tag.POS
        if pos == "VERB":
            pos = '5'
        elif pos == "NOUN":
            pos = '1'
        elif pos == "ADJF":
            pos = '2'
        elif pos == "ADJS":
            pos = '3'
        elif pos == "COMP":
            pos = '4'
        elif pos == "INFN":
            pos = '6'
        elif pos == "PRTF":
            pos = '7'
        elif pos == "PRTS":
            pos = '8'
        elif pos == "GRND":
            pos = '9'
        elif pos == "NUMR":
            pos = '0'
        elif pos == "ADVB":
            pos = 'a'
        elif pos == "NPRO":
            pos = 'b'
        elif pos == "PRED":
            pos = 'c'
        elif pos == "PREP":
            pos = 'd'
        elif pos == "CONJ":
            pos = 'e'
        elif pos == "PRCL":
            pos = 'f'
        elif pos == "INTJ":
            pos = 'g'
        else:
            pos = ' '
        singular = p[i].tag.number
        if singular == "sing":
            singular = 'Y'
        elif singular == "plur":
            singular = 'N'
        else:
            singular = ' '
        kind = p[i].tag.gender
        if kind == "femn":
            kind = 'F'
        elif kind == "masc":
            kind = 'M'
        elif kind == 'neut':
            kind = 'N'
        else:
            kind = ' '
        cow = p[i].tag.case
        if cow == "nomn":
            cow = '1'
        elif cow == "gent":
            cow = '2'
        elif cow == "datv":
            cow = '3'
        elif cow == "accs":
            cow = '4'
        elif cow == "ablt":
            cow = '5'
        elif cow == "loct":
            cow = '6'
        elif cow == "voct":
            cow = '7'
        elif cow == "gen2":
            cow = '8'
        elif cow == "acc2":
            cow = '9'
        elif cow == "loc2":
            cow = '0'
        else:
            cow = ' '
        print("{}: часть речи - {}, единственное число? - {}, род - {}, падеж - {}".format(p[i].word, pos, singular, kind, cow))
        
print("Введите слово")
word = input()
new_w(word)

