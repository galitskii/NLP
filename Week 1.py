# coding: utf-8
# *Работа с базой данных*
# https://oracle.github.io/python-cx_Oracle/
import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()
cur.execute("SELECT * FROM CASE_OF_WORD")
rows = cur.fetchall()
for row in rows:
        print("{0} {1}".format(row[0], row[1]))
myconnection.close()


# # токенайзер

import re
split_sent = re.compile(r'[.|!|?|…|?!]')
split_w = re.compile('([^\w_-]|[+])', re.U)

def simple_sent_tokenize(text):
    sent = []
    sentences = filter(lambda t: t, [t.strip() for t in split_sent.split(text)])
    for s in sentences:
        sent.append(s)
    return sent

def simple_word_tokenize(text):
    return [t for t in split_w.split(text) if t and not t.isspace() and t is not ',' and t is not '«' and t is not '»']

def s_words_tokenize(text):
    t = []
    for i in text:
        t.extend(simple_word_tokenize(i))
    t = list(set(t))
    return t

text = '''Министерство иностранных дел Азербайджана заявило, что российский вертолет сбили азербайджанские военные. Это произошло «в свете напряженной обстановки в регионе и повышенной боевой готовности в связи с возможными провокациями армянской стороны», сообщило ведомство.

В МИДе пояснили, что полет вертолета проходил в непосредственной близости от армяно-азербайджанской границы на фоне продолжающихся военных действий в Нагорном Карабахе. Также в Баку отметили, что вертолет летел в темное время суток и что воздушная техника ВВС России ранее не была замечена в этом районе.

Азербайджан «приносит извинения российской стороне в связи с данным трагическим инцидентом, который носит характер случайности». Баку также выразил соболезнования семьям погибших и пожелал скорейшего выздоровления пострадавшему. Азербайджан?!'''

print(text)

text = text.lower()
print(text)
sent = simple_sent_tokenize(text)
print(sent)
words = s_words_tokenize(sent)
print(words)
print("Количество слов в списке = ", len(words))


# # алгоритм
import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()
cur.execute("SELECT * FROM new_words")
rows = cur.fetchall()
for row in rows:
        print("{0} {1}".format(row[0], row[1]))
myconnection.close()


# # HTML
# библиотеки для запросов
import requests as req
from urllib.request import urlopen
from lxml import etree

# веб-страница
url = 'https://news.mail.ru/economics/44178288/?frommail=1'

headers = {'Content-Type': 'text/html',}

reqs = req.get(url, headers=headers)

html = reqs.text

with open ('req', 'w', encoding='utf-8') as f:
    f.write(html)
f.close()

from bs4 import BeautifulSoup

# пример работы с html

soup = BeautifulSoup("<p>Some<b>bad<i>HTML", "lxml")

# печать с абзацами

print(soup.prettify())

soup.find(text="bad")

soup.p

soup = BeautifulSoup("<tag1>Some<tag2/>bad<tag3>XML", "xml")

print(soup.prettify())

for child in soup.recursiveChildGenerator():
    if child.name:
        print(child.name)

root = soup.p

# ищем потомков root
root_childs = [e.name for e in root.children if e.name is not None]
print(root_childs)

# получаем всех потомков
root = soup.body
root_childs = [e.name for e in root.descendants if e.name is not None]
print(root_childs)

# веб-страница
url = 'https://news.mail.ru/economics/44178288/?frommail=1'

reqs = req.get(url)

soup = BeautifulSoup(reqs.text, 'lxml')
print(soup.title)
print(soup.title.text)
# print(soup.title.parent)