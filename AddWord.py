'''
Кусок программы, которая позволит добавлять новые слова в базу.
На вход даём слово. Если образованных от него слов нет, то 
он запишет его родителя в базу. Для остальных случаев пока не отлажено

Для этого создаётся таблица words_q, в которой добавлен вид (совершенный, ...)

Пока работаем в MySQL
'''
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def new_w(word):
    p = morph.parse(word)
    res = list()
    for i in range(len(p)):
        pos = p[i].tag.POS # часть речи
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
            pos = ''
        singular = p[i].tag.number # число
        if singular == "sing":
            singular = 'Y'
        elif singular == "plur":
            singular = 'N'
        else:
            singular = ''
        kind = p[i].tag.gender # род
        if kind == "femn":
            kind = 'F'
        elif kind == "masc":
            kind = 'M'
        elif kind == "neut":
            kind = 'N'
        else:
            kind = ''
        cow = p[i].tag.case # падеж
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
            cow = ''
        tense =  p[i].tag.tense # время
        if tense == "past":
            tense = 'P'
        elif tense == "pres":
            tense =  'C'
        elif tense == "futr":
            tense = 'F'
        else:
            tense = ''
        animal = p[i].tag.animacy # одушевлённость 
        if animal == "anim":
            animal = 'Y'
        elif animal == "inan":
            animal = 'N'
        else:
            animal = ''
        person = p[i].tag.person # лицо
        if person == "1per":
            person = '1'
        elif person == "2per":
            person = '2'
        elif person == "3per":
            person = '3'
        else:
            person = ''
        perf = p[i].tag.aspect # вид
        if perf == "perf":
            perf = 'Y'
        elif perf == "impf":
            perf = 'N'
        else:
            perf = ''
        main = p[i].normal_form        
        l = (p[i].word, pos, singular, kind, cow, tense, animal, person, perf, main)
        res.append(l)
    return res

import mysql.connector
from mysql.connector import Error

conn = mysql.connector.connect(host='localhost', user='lexis', password='lexis', database = 'lexis')
cur = conn.cursor()

def add_w(word):
    for w in new_w(word):
        cur.execute("select * from words_q where word = '{}'".format(w[9]))
        rows = cur.fetchall()
        print(len(rows))
        if len(rows) == 0:
            cur.execute("select max(mid) from words_q")
            num = cur.fetchall()
            if not (num[0][0]):
                num = 1
            else:
                num = int(num[0][0]) + 1
            cur.execute("insert into words_q(word, mid, fid, pos, singular, kind, cow, tense, animal, person, perf) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(w[0], num, 0, w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8]))
        else:            
            for m in rows:
                print(m)
                cur.execute("select * from words_q where word = '{}'".format(word))
                print(m[0])
                q = cur.fetchall()
                q = set(q)
                if m in q:
                    print("Exist")

print("Введите слово")
word = input()
add_w(str(word))

conn.commit()
conn.close()

