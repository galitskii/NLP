
# coding: utf-8

# # Добавление новых слов в NEW_WORDS

# In[141]:


# https://oracle.github.io/python-cx_Oracle/
import cx_Oracle


# In[142]:


myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')


# In[143]:


cur = myconnection.cursor()


# In[145]:


# выводим список таблиц
cur.execute("select table_name from USER_TABLES")
res = cur.fetchall()
for row in res:
        print("{0}".format(row[0]))


# In[147]:


# выводим список столбцов NEW_WORDS
cur.execute("select column_name from user_tab_columns where table_name = 'NEW_WORDS'")
res = cur.fetchall()
for row in res:
        print("{0}".format(row[0]))


# In[160]:


# получаем список новых слов
cur.execute("select WORD from NEW_WORDS")
res = cur.fetchall()
for row in res:
        print("{0}".format(row[0]))


# ## Дальше исполняем код токенайзера

# In[158]:


# проверяем, есть ли среди words новые слова. Если да, то есть ли они в new_words. Если нет, добавляем их в new_words
for word in words:
    cur.execute("select MID, WORD from WORDS where WORD = '%s'" % word)
    res = cur.fetchall()
    if len(res) == 0:
        cur.execute("select WORD from NEW_WORDS where WORD = '%s'" % word)
        res2 = cur.fetchall()
        if len(res2) == 0:
            cur.execute("insert into NEW_WORDS(WORD) values ('%s')" % word)


# In[159]:


# сохраняем изменения
myconnection.commit()


# In[161]:


# закрываем соединение
myconnection.close()


# # токенайзер

# In[149]:


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


# In[150]:


text = '''Министерство иностранных дел Азербайджана заявило, что российский вертолет сбили азербайджанские военные. Это произошло «в свете напряженной обстановки в регионе и повышенной боевой готовности в связи с возможными провокациями армянской стороны», сообщило ведомство.

В МИДе пояснили, что полет вертолета проходил в непосредственной близости от армяно-азербайджанской границы на фоне продолжающихся военных действий в Нагорном Карабахе. Также в Баку отметили, что вертолет летел в темное время суток и что воздушная техника ВВС России ранее не была замечена в этом районе.

Азербайджан «приносит извинения российской стороне в связи с данным трагическим инцидентом, который носит характер случайности». Баку также выразил соболезнования семьям погибших и пожелал скорейшего выздоровления пострадавшему. Азербайджан?!'''


# In[151]:


print(text)


# In[152]:


text = text.lower()


# In[153]:


print(text)


# In[154]:


sent = simple_sent_tokenize(text)


# In[155]:


print(sent)


# In[156]:


words = s_words_tokenize(sent)


# In[157]:


print(words)
print("Количество слов в списке = ", len(words))


# # HTML

# In[90]:


# библиотеки для запросов
import requests as req
from urllib.request import urlopen
from lxml import etree


# In[64]:


# веб-страница
url = 'https://news.mail.ru/economics/44178288/?frommail=1'


# In[46]:


headers = {'Content-Type': 'text/html',}


# In[47]:


reqs = req.get(url, headers=headers)


# In[48]:


html = reqs.text


# In[49]:


with open ('req', 'w', encoding='utf-8') as f:
    f.write(html)


# In[69]:


f.close()


# In[50]:


from bs4 import BeautifulSoup


# In[83]:


# пример работы с html

soup = BeautifulSoup("<p>Some<b>bad<i>HTML", "lxml")


# In[79]:


# печать с абзацами

print(soup.prettify())


# In[53]:


soup.find(text="bad")


# In[73]:


soup.p


# In[74]:


soup = BeautifulSoup("<tag1>Some<tag2/>bad<tag3>XML", "xml")


# In[75]:


print(soup.prettify())


# In[80]:


for child in soup.recursiveChildGenerator():
    if child.name:
        print(child.name)


# In[85]:


root = soup.p


# In[87]:


# ищем потомков root
root_childs = [e.name for e in root.children if e.name is not None]
print(root_childs)


# In[88]:


# получаем всех потомков
root = soup.body
root_childs = [e.name for e in root.descendants if e.name is not None]
print(root_childs)


# In[89]:


# веб-страница
url = 'https://news.mail.ru/economics/44178288/?frommail=1'


# In[91]:


reqs = req.get(url)


# In[98]:


soup = BeautifulSoup(reqs.text, 'lxml')
print(soup.title)
print(soup.title.text)
# print(soup.title.parent)

