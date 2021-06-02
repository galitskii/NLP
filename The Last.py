import cx_Oracle
myconnection = cx_Oracle.connect('lexis/lexis@93.175.29.93/mipt')
cur = myconnection.cursor()

# функция возвращает список, полученный из исходной строки путём разбиения на слова и знаки пунктуации и приведения всего 
# к нижнему регистру
def space(str1):
    str1 = str1.lower()
    str2 = ''
    for i in range(len(str1)):
        if str1[i] in [',', '.', ';']:
            str2 += ' '
        str2 += str1[i]
    if str2[len(str2) - 1] == ' ':
        str2 = str2[:len(str2) - 1]
    return str2.split()

# функция проверяет сочетания из 4 подряд идущих слов в списке lst
# во всех таких ситуациях exception не учитываем
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
        for i1 in res1:
            for i2 in res2:
                for i3 in res3:
                    for i4 in res4:
                        cur.execute("select ans from add4_r where prt_1 = '{}' and sing_1 = '{}' and cow_1 = '{}' and prt_2 = '{}' and sing_2 = '{}' and cow_2 = '{}' and prt_3 = '{}' and sing_3 = '{}' and cow_3 = '{}' and prt_4 = '{}' and sing_4 = '{}' and cow_4 = '{}'".format(i1[0], i1[1], i1[2], i2[0], i2[1], i2[2], i3[0], i3[1], i3[2], i4[0], i4[1], i4[2]))
                        res = cur.fetchall()
                        res = list(set(res))
                        if len(res) > 0:
                            for r in res:
                                result.append(r[0])
        result = list(set(result))
        if len(result) > 0:
            if 'N' in result:
                print("OK4", result)
                return ["N"]
        print("OK4", result)
        return result
    
# функция проверяет сочетания из 3 подряд идущих слов в списке lst
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
                    print("OK3", result)
                    return ['N']
    print("OK3", result)
    return result

# функция проверяет сочетания из 2 подряд идущих слов в списке lst
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
                        print(k[3])
        if 'Y' in ans1:
            result.append('Y')
        elif 'N' in ans1:
            result.append('N')
        else:
            result.append('E')
    print("ОК2", result)
    return result

def comma(l):
    while ('и' in l):
        id = l.index('и')
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id - 1])
        res_l = cur.fetchall()
        res_l = list(set(res_l))
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id + 1])
        res_r = cur.fetchall()
        res_r = list(set(res_r))
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
            if (part in ['1', 'b']) and time == 'Y':
                l.insert(id, 'он')
            elif (part in ['1', 'b']) and time == 'N':
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

def check(l):
    result = []
    while 'и' in l or 'или' in l:
        l = comma(l)
    # когда в предложении нет И или ИЛИ
    print(l)
    if len(l) > 3:
        result += four(l)
    if len(l) > 2:
        result += three(l)
    if len(l) > 1:
        result += two(l)
    if len(l) == 1:
        result += ['Y']    # если предложение из одного слова, оно не может быть неверным с точки зрения согласования
                        # единственного и множественнго числа
    print("OK_CHECK", result)
    return result

def res(r):
    if 'N' in r:
        print("Ошибка в согласовании единственного и множественного числа")
    elif 'Y' in r:
        print("Ошибок в согласовании единственного и множественного числа не обнаружено")
    else:
        print("Есть незнакомые сочетания")
            
print("Введите предложение из слов, являющихся местоимением, существительным или глаголом (возможно перечисление инфинитивов или инфинитивов + существительное):")
str1 = input()

res(check(space(str1)))

myconnection.close()