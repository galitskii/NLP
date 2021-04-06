'''
программа получает на вход предложение, и начинает заменять части одного,
связанные и (или) и разделённые запятыми
'''

import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()

def comma(l):
    while ('и' in l):
        id = l.index('и')
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id - 1])
        res_l = cur.fetchall()
        res_l = list(set(res_l))
        #print(res_l)
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id + 1])
        res_r = cur.fetchall()
        res_r = list(set(res_r))
        #print(res_r)
        err = 0
        part = ' '
        part2 = ' '
        time = ' '
        for i in res_l:
            for j in res_r:
                if ((i[0] == j[0]) or (i[0] == '1' and j[0] == 'b') or (i[0] == 'b' and j[0] == '1')) and (i[1] == j[1]):
                    err = 1
                    part = i[0]
                    part2 = j[0]
                    time = i[1]
             #       print(part)
        if err == 0:
            print("Ошибка в согласовании")
            #break
            return(['я', 'рубили'])
        else:
            left = 0
            i = id - 1
            while (i - 2 >= 0 and l[i - 1] == ','):
                cur.execute("select pos, singular, cow from words where word = '%s'" % l[i - 2])
                res_r = cur.fetchall()
                res_r = list(set(res_r))
                for q in res_r:
                    if (part == q[0] or part == j[0]) and (time == q[1]):
                        left = i - 2
                    else:
                        return(['я', 'рубили'])
                i = i - 2
            l.pop(id)
            if (part in ['1', 'b']):
                l.insert(id, 'они')
            elif (part == '5') and time == 'N':
                l.insert(id, 'делали')
            elif part == '5' and time == 'Y':
                l.insert(id, 'делал')
            elif part == '6':
                l.insert(id, 'быть')
            l.pop(id + 1)
            for j in range(id - i):
                l.pop(i)
    while ('или' in l):
        id = l.index('или')
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id - 1])
        res_l = cur.fetchall()
        res_l = list(set(res_l))
        #print(res_l)
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id + 1])
        res_r = cur.fetchall()
        res_r = list(set(res_r))
        #print(res_r)
        err = 0
        part = ' '
        part2 = ' '
        time = ' '
        for i in res_l:
            for j in res_r:
                if ((i[0] == j[0]) or (i[0] == '1' and j[0] == 'b') or (i[0] == 'b' and j[0] == '1')) and (i[1] == j[1]):
                    err = 1
                    part = i[0]
                    part2 = j[0]
                    time = i[1]
             #       print(part)
        if err == 0:
            print("Ошибка в согласовании")
            #break
            return(['я', 'рубили'])
        else:
            left = 0
            i = id - 1
            while (i - 2 >= 0 and l[i - 1] == ','):
                cur.execute("select pos, singular, cow from words where word = '%s'" % l[i - 2])
                res_r = cur.fetchall()
                res_r = list(set(res_r))
                for q in res_r:
                    if (part == q[0] or part == j[0]) and (time == q[1]):
                        left = i - 2
                    else:
                        return(['я', 'рубили'])
                i = i - 2
            l.pop(id)
            if (part in ['1', 'b']):
                l.insert(id, 'они')
            elif (part == '5') and time == 'N':
                l.insert(id, 'делали')
            elif part == '5' and time == 'Y':
                l.insert(id, 'делал')
            elif part == '6':
                l.insert(id, 'быть')
            l.pop(id + 1)
            for j in range(id - i):
                l.pop(i)
    print(l)
    
print("Введите предложение, состоящее из местоимений, личных глаголов, инфинитивов или существительных:")
str1 = input()
l =str1.split()
comma(l)

myconnection.close()