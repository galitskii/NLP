import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()

# функция возвращает строку, расставив пробелы между знаками препинания
def space(str1):
    str2 = ''
    for i in range(len(str1)):
        if str1[i] in [',']:
            str2 += ' '
        str2 += str1[i]
    return str2
    
def comma(l):
    l = l.split()
    if 'и' in l:
        id = l.index('и')
        part = []
        if l[id - 2] == ',':
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id - 1])
            res_l = cur.fetchall()
            res_l = list(set(res_l))
            #print(res_l)
            for i in res_l:
                if i[0] == '5':
                    part = part + ['5']
                elif i[0] == '1':
                    part = part + ['1']
                elif i[0] == '6':
                    part = part + ['6']
                elif i[0] == 'b':
                    part = part + ['b']
        part = list(set(part))
        #print(part)
        if '6' in part:
            cur.execute("select pos, singular, cow from words where word = '%s'" % l[id + 1])
            res1 = cur.fetchall()
            res1 = list(set(res1))
            #print(res1)
            if id + 2 < len(l):
                cur.execute("select pos, singular, cow from words where word = '%s'" % l[id + 2])
                res2 = cur.fetchall()
                res2 = list(set(res2))
                #print(res2)
            if id + 3 < len(l):
                cur.execute("select pos, singular, cow from words where word = '%s'" % l[id + 3])
                res3 = cur.fetchall()
                res3 = list(set(res3))
                #print(res3)
            for j in res1:
                if j[0] == '6':
                    #print("OK")
                    break
            q = id
            while q > 0:
                cor = 0
                if (l[q - 2] == ','):
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[q - 1])
                    res4 = cur.fetchall()
                    res4 = list(set(res4))
                    for s in res4:
                        if s[0] == '6':
                            cor = 1
                            break
                    if cor == 1:
                        q = q - 2
                    else:
                        return ['N']
                    #print(res4, "!!!")
                elif (l[id - 2] == ','):
                    q = id - 3
                elif (l[id - 2] == ','):
                    q = id - 4
                q = -1
    return l
    
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
        #print(res_l, res_r)
        for i in res_l:
            for j in res_r:
                cur.execute("select ans, comm, ex, r_id from simple_rules where prt_l = '{}' and prt_r = '{}' and sing_l = '{}' and sing_r = '{}' and cow_l = '{}' and cow_r = '{}'".format(i[0], j[0], i[1], j[1], i[2], j[2]))
                res = cur.fetchall()
                res = list(set(res))
                #print(res)
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

def three(lst):
    result = []
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
                    return ['N']
    return result
    
def four(lst):
    result = []
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
                    return ['N']
    return result

def run(str1):
    str1 = str1.lower()
    lst = comma(space(str1)) # делаем строку списком
    res = []
    if len(lst) > 3:
        res = res + four(lst)
    if len(lst) > 2:
        res = res + three(lst)
    if len(lst) > 1:
        res  = res + two(lst)
    print(res)
    res = list(set(res))
    if 'N' in res:
        print("Ошибка в согласовании единственого и множественного числа")
    elif 'Y' in res:
        print("Ошибок в согласовании единственого и множественного числа нет")
        
print("Введите предложение из слов, являющихся местоимением, существительным или глаголом без запятыз или с запятыми, если перечисляется по 1 инфинитиву:")
str1 = input()
run(str1)