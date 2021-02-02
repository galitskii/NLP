"""
здесь реализована функция check, которая на вход принимает строку str, 
состоящую из 2 слов, являющихся местоимением, существительным или глаголом,
и проверяет, согласовано ли в этой паре слов число. 

После этого функция res обрабатывает данные, полученные check, 
и принимает решение
"""

import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()

def check(str):
    lst = str.split() # разбиваем предложение на слова
    if len(lst) != 2:
        print("Это не пара слов")
        return -1
    
    cur.execute("select pos, singular from words where word = '%s'" % lst[0])
    res_l = cur.fetchall()
    res_l = list(set(res_l))

    cur.execute("select pos, singular from words where word = '%s'" % lst[1])
    res_r = cur.fetchall()
    res_r = list(set(res_r))

    ans = [] # здесь будут варианты ответа
    
    for i in res_l:
        for j in res_r:
            #print("select ans from simple_rules where prt_l = '{}' and prt_r = '{}' and sing_l = '{}' and sing_r = '{}'".format(i[0], j[0], i[1], j[1]))
            cur.execute("select ans from simple_rules where prt_l = '{}' and prt_r = '{}' and sing_l = '{}' and sing_r = '{}'".format(i[0], j[0], i[1], j[1]))
            res = cur.fetchall()
            res = list(set(res))
            if len(res) > 0:
                for k in res:
                    ans.append(k[0])
    return set(ans)

def res(str):
    l = check(str)
    if 'Y' in l:
        print("Ошибок в согласовании единственного и множественного числа нет")
    elif 'N' in l:
        print("Ошибка в согласовании числа")
    else:
        print("Ни одно правило не сработало")

print("Введите словосочетание, состоящее из 2 слов, являющихся местоимением, существительным или глаголом:")
str1 = input()
res(str1)

myconnection.close()