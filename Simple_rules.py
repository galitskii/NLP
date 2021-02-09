"""
здесь реализована функция check, которая на вход принимает строку str, 
состоящую из слов, являющихся местоимением, существительным или глаголом (без знаков пунктуации),
и проверяет, согласовано ли число в этой строке. 

После этого функция res обрабатывает данные, полученные check, 
и принимает решение
"""

import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()

def check(str):
    lst = str.split() # разбиваем предложение на слова
    
    ans = [] # здесь будут варианты ответа
    
    for q in range(len(lst) - 1):
        ans1 = [] 
        cur.execute("select pos, singular, cow from words where word = '%s'" % lst[q])
        res_l = cur.fetchall()
        res_l = list(set(res_l))

        cur.execute("select pos, singular, cow from words where word = '%s'" % lst[q + 1])
        res_r = cur.fetchall()
        res_r = list(set(res_r))
    
        for i in res_l:
            for j in res_r:
            #print("select ans from simple_rules where prt_l = '{}' and prt_r = '{}' and sing_l = '{}' and sing_r = '{}'".format(i[0], j[0], i[1], j[1]))
                cur.execute("select ans from simple_rules where prt_l = '{}' and prt_r = '{}' and sing_l = '{}' and sing_r = '{}' and cow_l = '{}' and cow_r = '{}'".format(i[0], j[0], i[1], j[1], i[2], j[2]))
                res = cur.fetchall()
                res = list(set(res))

                if len(res) > 0:
                    for k in res:
                        ans1.append(k[0])                        
        if 'Y' in ans1:
            ans.append('Y')
        elif 'N' in ans1:
            ans.append('N')
        else:
            ans.append('E')
    print("Результат прохода: ", ans)
    return set(ans)

def res(str):
    l = check(str)
    if 'E' in l:
        print("Есть незнакакомые сочетания")
    elif 'N' in l:
        print("Ошибка в согласовании единственного и множественного числа")
    else:
        print("Ошибок в согласовании единственного и множественного числа нет")

print("Введите предложение из слов, являющихся местоимением, существительным или глаголом без использования знаков пунктуации:")
str1 = input()
res(str1)

myconnection.close()