"""
здесь реализована функция check, которая на вход принимает строку str,
состоящую из предложений, которые, в свою очередь, являющихся местоимением, существительным или глаголом (разделённые точкой),
и проверяет, согласовано ли число в этой строке. 

функция str_p отделяет от слов запятые

После этого функция res обрабатывает данные, полученные check, 
и принимает решение
"""
import cx_Oracle

myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')

cur = myconnection.cursor()

def str_p(l):
    l1 = []
    for i in l:
        if i.find(',') != -1:
            l1.append(i[0:-1])
            l1.append(',')
        else:
            l1.append(i)
    return l1

def check(str):
    lst = str.split() # разбиваем предложение на слова
    lst = str_p(lst) # отделяем запятые
    result = [] # здесь будут варианты ответа
    #prep = []
    #pand = []
    #k = 0
    #for i in lst:
    #    if i == ',':
    #        prep.append(k)
    #    elif i == 'и':
    #        pand.append(k)
    #    k += 1
    if len(lst) > 3:
        for i in range(0, len(lst) - 3):
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i])
            res1 = cur.fetchall()
            res1 = list(set(res1))
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i + 1])
            res2 = cur.fetchall()
            res2 = list(set(res2))
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i + 2])
            res3 = cur.fetchall()
            res3 = list(set(res3))
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i + 3])
            res4 = cur.fetchall()
            res4 = list(set(res4))
            if len(res1) > 0:
                for i1 in res1:
                    for i2 in res2:
                        for i3 in res3:
                            for i4 in res4:
                                cur.execute("select ans from add4_r where prt_1 = '{}' and sing_1 = '{}' and cow_1 = '{}' and prt_2 = '{}' and sing_2 = '{}' and cow_2 = '{}' and prt_3 = '{}' and sing_3 = '{}' and cow_3 = '{}' and prt_4 = '{}' and sing_4 = '{}' and cow_4 = '{}'".format(i1[0], i1[1], i1[2], i2[0], i2[1], i2[2],i3[0], i3[1], i3[2],i4[0], i4[1], i4[2]))
                                res = cur.fetchall()
                                res = list(set(res))
                                if len(res) > 0:
                                    for r in res:
                                        result.append(r[0])
            result = list(set(result))
            if len(result) > 0:
                if 'N' in result:
                    return result
    if len(lst) > 2:
        for i in range(0, len(lst) - 2):
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i])
            res1 = cur.fetchall()
            res1 = list(set(res1))
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i + 1])
            res2 = cur.fetchall()
            res2 = list(set(res2))
            cur.execute("select pos, singular, cow from words where word = '%s'" % lst[i + 2])
            res3 = cur.fetchall()
            res3 = list(set(res3))
            if len(res1) > 0:
                for i1 in res1:
                    for i2 in res2:
                        for i3 in res3:
                            cur.execute("select ans from add3_r where prt_1 = '{}' and sing_1 = '{}' and cow_1 = '{}' and prt_2 = '{}' and sing_2 = '{}' and cow_2 = '{}' and prt_3 = '{}' and sing_3 = '{}' and cow_3 = '{}'".format(i1[0], i1[1], i1[2], i2[0], i2[1], i2[2],i3[0], i3[1], i3[2]))
                            res = cur.fetchall()
                            res = list(set(res))
                            if len(res) > 0:
                                for r in res:
                                    result.append(r[0])
            result = list(set(result))
            if len(result) > 0:
                if 'N' in result:
                    return result
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
                cur.execute("select ans, comm, ex, r_id from simple_rules where prt_l = '{}' and prt_r = '{}' and sing_l = '{}' and sing_r = '{}' and cow_l = '{}' and cow_r = '{}'".format(i[0], j[0], i[1], j[1], i[2], j[2]))
                res = cur.fetchall()
                res = list(set(res))

                if len(res) > 0:
                    for k in res:
                        ans1.append(k[0]) 
        if 'Y' in ans1:
            result.append('Y')
        elif 'N' in ans1:
            result.append('N')
        else:
            result.append('E')
    print("Результат прохода: ", result)
    return set(result)

def spl(str):
    l = check(str)
    if 'E' in l:
        print("Есть незнакакомые сочетания")
    elif 'N' in l:
        print("Ошибка в согласовании единственного и множественного числа")
    else:
        print("Ошибок в согласовании единственного и множественного числа нет")

def res(str):
    l = str.split(".")
    for i in l:
        if i.split() != []:
            spl(i)



print("Введите предложение из слов, являющихся местоимением, существительным или глаголом без использования знаков пунктуации:")
str1 = input()
res(str1)

myconnection.close()