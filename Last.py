import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()

# функция возвращает строку, расставив пробелы между знаками препинания; 
# приводит всё к нижнему регистру
def space(str1):
    str1 = str1.lower()
    str2 = ''
    for i in range(len(str1)):
        if str1[i] in [',']:
            str2 += ' '
        str2 += str1[i]
    return str2

def two(lst):
    result = []
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
    return result

def comma(l):
    l = l.split()
    llen = len(l)
    h = -1
    t = -1
    if 'и' in l:
        id1 = l.index('и')
        if l[id1 - 2] == ',' and id1 - 2 >= 0:
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 1])
            res1 = cur.fetchall()
            for i in res1:
                part = i[0]
                h = id1 - 1
                t = id1
                if part == '6':
                    if id1 + 1 < llen:
                        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 1])
                        res2 = cur.fetchall()
                        for j in res2:
                            if j[0] == part:
                                t = id1 + 1
                                break
                        idpr = id1 - 2
                        idd = False
                        while idpr >= 0:
                            if l[idpr] == ',':
                                cur.execute("select pos, singular, cow from words where word = '%s'" % l[idpr + 1])
                                res2 = cur.fetchall()
                                for j in res2:
                                    if j[0] == part:
                                        l[idpr] = '`'
                                        h = idpr
                                        idpr = idpr - 2
                                        idd = True
                                        break
                            elif l[idpr - 1] == ',':
                                anss = two(l[idpr] + l[idpr + 1])
                                if 'N' in anss:
                                    return ["Он", "учили"]
                                elif 'Y' in anss:
                                    h = idpr - 2
                                    idpr = idpr - 1
                                    idd = True
                            elif idd:
                                break
                    l = l[0 : h - 1] + ['учиться'] + l[t + 1 :]
        elif l[id1 - 3] == ',' and id1 - 3 >= 0:
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 2])
            res1 = cur.fetchall()
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 1])
            res2 = cur.fetchall()
            for i in res1:
                for j in res2:
                    part1 = i[0]
                    part2 = j[0]
                    s1 = i[1]
                    s2 = j[1]
                    c1 = i[2]
                    c2 = j[2]
                    if part1 == '6': # идентифицировал, что словосочетание из двух слов, левое - инфинитив
                        h = id1 - 2
                        t = id1
                        if id1 + 1 < llen:
                            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 1])
                            res3 = cur.fetchall()
                            for k in res3:
                                if k[0] == part1:
                                    t = id1 + 1
                                    break
                        idd = False
                        idpr = id1 - 5
                        while idpr >= 0:
                            if l[idpr] == ',':
                                h = idpr + 1
                                idd = True
                                idpr = idpr - 2
                            elif idpr - 1 >= 0 and l[idpr - 1] == ',':
                                h = idpr
                                idd = True
                                idpr = idpr - 3
                            else:
                                break
                        idb = False # индикатор того, что сработало правило для начала перечисления
                        if l[h - 1] == ',':
                            cur.execute("select pos, singular, cow from words where word = '%s'" % l[h - 2])
                            res3 = cur.fetchall()
                            for k in res3:
                                if k[0] == part1:
                                    h = h - 2
                                    idb = True
                                    break
                        if h - 3 >= 0 and l[h - 1] == ',' and not(idb):
                            cur.execute("select pos, singular, cow from words where word = '%s'" % l[h - 3])
                            res3 = cur.fetchall()
                            for k in res3:
                                if k[0] == part1:
                                    h = h - 3
                                    idb = True
                                    break
                        if h - 4 >= 0 and l[h - 1] == ',' and not(idb):
                            cur.execute("select pos, singular, cow from words where word = '%s'" % l[h - 4])
                            res3 = cur.fetchall()
                            for k in res3:
                                if k[0] == part1:
                                    h = h - 4
                                    idb = True
                                    break
                        return l[:h] + ['учиться'] + l[t + 1:]
        elif id1 - 4 >= 0 and l[id1 - 4] == ',':
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 3])
            res1 = cur.fetchall()
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 2])
            res2 = cur.fetchall()
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 1])
            res3 = cur.fetchall()
            for i in res1:
                for j in res2:
                    for k in res3:
                        part1 = i[0]
                        part2 = j[0]
                        part3 = k[0]
                        s1 = i[1]
                        s2 = j[1]
                        s3 = k[1]
                        c1 = i[2]
                        c2 = j[2]
                        c3 = k[2]
                        if i[0] == '6':
                            h = id1 - 3
                            t = id1
                            if id1 + 1 < llen:
                                cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 1])
                                res4 = cur.fetchall()
                                for q in res4:
                                    if q[0] == part1:
                                        t = id1 + 1
                                        break
                            idpr = id1 - 6
                            idd = False
                            while idpr >= 0:
                                if l[idpr] == ',':
                                    h = idpr + 1
                                    idd = True
                                    idpr = idpr - 2
                                elif idpr - 1 >= 0 and l[idpr - 1] == ',':
                                    h = idpr
                                    idd = True
                                    idpr = idpr - 3
                                elif idpr - 2 >= 0 and l[idpr - 2] == ',':
                                    h = idpr - 1
                                    idd = True
                                    idpr = idpr - 4
                                else:
                                    break
                            idb = False # индикатор того, что сработало правило для начала перечисления
                            if l[h - 1] == ',':
                                cur.execute("select pos, singular, cow from words where word = '%s'" % l[h - 2])
                                res4 = cur.fetchall()
                                for q in res4:
                                    if q[0] == part1:
                                        h = h - 2
                                        idb = True
                                        break
                            if h - 3 >= 0 and l[h - 1] == ',' and not(idb):
                                cur.execute("select pos, singular, cow from words where word = '%s'" % l[h - 3])
                                res4 = cur.fetchall()
                                for q in res4:
                                    if q[0] == part1:
                                        h = h - 3
                                        idb = True
                                        break
                            if h - 4 >= 0 and l[h - 1] == ',' and not(idb):
                                cur.execute("select pos, singular, cow from words where word = '%s'" % l[h - 4])
                                res4 = cur.fetchall()
                                for q in res4:
                                    if q[0] == part1:
                                        h = h - 4
                                        idb = True
                                        break
                            return l[:h] + ['учиться'] + l[t + 1:]
    return l

def check(lst):
    result = [] # здесь будут варианты ответа
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
    if len(str) == len(l):
        if 'E' in l:
            print("Есть незнакакомые сочетания")
        elif 'N' in l:
            print("Ошибка в согласовании единственного и множественного числа")
        else:
            print("Ошибок в согласовании единственного и множественного числа нет")
    else:
        if 'N' in l:
            print("Ошибка в согласовании единственного и множественного числа")
        elif 'Y' in l:
            print("Ошибок в согласовании единственного и множественного числа нет")
        else:
            print("Есть незнакакомые сочетания")
            
print("Введите предложение из слов, являющихся местоимением, существительным или глаголом (возможно перечисление инфинитивов или инфинитивов + существительное):")
str1 = input()
spl(comma(space(str1)))

myconnection.close()