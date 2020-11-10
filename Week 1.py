
# coding: utf-8

# *Работа с базой данных*

# In[1]:


# https://oracle.github.io/python-cx_Oracle/
import cx_Oracle


# In[10]:


myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')


# In[11]:


cur = myconnection.cursor()


# In[12]:


cur.execute("SELECT * FROM CASE_OF_WORD")


# In[13]:


rows = cur.fetchall()


# In[14]:


for row in rows:
        print("{0} {1}".format(row[0], row[1]))


# In[15]:


myconnection.close()


# # токенайзер

# In[20]:


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


# In[21]:


text = '''Министерство иностранных дел Азербайджана заявило, что российский вертолет сбили азербайджанские военные. Это произошло «в свете напряженной обстановки в регионе и повышенной боевой готовности в связи с возможными провокациями армянской стороны», сообщило ведомство.

В МИДе пояснили, что полет вертолета проходил в непосредственной близости от армяно-азербайджанской границы на фоне продолжающихся военных действий в Нагорном Карабахе. Также в Баку отметили, что вертолет летел в темное время суток и что воздушная техника ВВС России ранее не была замечена в этом районе.

Азербайджан «приносит извинения российской стороне в связи с данным трагическим инцидентом, который носит характер случайности». Баку также выразил соболезнования семьям погибших и пожелал скорейшего выздоровления пострадавшему. Азербайджан?!'''


# In[22]:


print(text)


# In[23]:


text = text.lower()


# In[24]:


print(text)


# In[25]:


sent = simple_sent_tokenize(text)


# In[26]:


print(sent)


# In[27]:


words = s_words_tokenize(sent)


# In[28]:


print(words)
print("Количество слов в списке = ", len(words))


# # алгоритм

# In[6]:


import cx_Oracle


# In[7]:


myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')


# In[14]:


cur = myconnection.cursor()


# In[15]:


cur.execute("SELECT * FROM new_words")


# In[18]:


print(type(cur))


# In[12]:


rows = cur.fetchall()


# In[17]:


print(type(rows))


# In[16]:


for row in rows:
        print("{0} {1}".format(row[0], row[1]))


# In[19]:


myconnection.close()

