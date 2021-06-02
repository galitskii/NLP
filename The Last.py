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
    part = []
    left = -1 # границы заменяемого диапазона
    right = -1
    print("И или ИЛИ")
    llen = len(l) # длина предложения
    id1 = l.index('и')
    print(id1)
    part = -1
    if llen > id1 + 1: # следующее за "И" слово
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 1])
        resp1 = cur.fetchall()
        resp1 = list(set(resp1))
    if llen > id1 + 2:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 2])
        resp2 = cur.fetchall()
        resp2 = list(set(resp2))
    if llen > id1 + 3:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 3])
        resp3 = cur.fetchall()
        resp3 = list(set(resp3))
    if llen > id1 + 4:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 + 4])
        resp4 = cur.fetchall()
        resp4 = list(set(resp4))
    if id1 - 1 >= 0:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 1])
        resl1 = cur.fetchall()
        resl1 = list(set(resl1))
    if id1 - 2 >= 0:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 2])
        resl2 = cur.fetchall()
        resl2 = list(set(resl2))
    if id1 - 3 >= 0:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 3])
        resl3 = cur.fetchall()
        resl3 = list(set(resl3))
    if id1 - 4 >= 0:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 4])
        resl4 = cur.fetchall()
        resl4 = list(set(resl4))
    if id1 - 5 >= 0:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 5])
        resl5 = cur.fetchall()
        resl5 = list(set(resl5))
    if id1 - 6 >= 0:
        cur.execute("select pos, singular, cow from words where word = '%s'" % l[id1 - 6])
        resl6 = cur.fetchall()
        resl6 = list(set(resl6))
    if id1 + 1 < llen:
        for i in resp1:
            if i[0] == '6':
                print("6")
                right = id1 + 1
                part = '6'
        if right == -1:
                for i in resp1:
                    if i[0] == '5':
                        print("5")
                        right = id1 + 1
                        part = '5'
                        sng = i[1]
                        break
    if part == '6':
        if id1 - 4 >= 0 and left == -1 and not (',' in l[id1 - 4: id1]): # это раньше, поскольку может быть 2 инфинитива
            for i in resl4:
                if i[0] == part:
                    r = check(l[id1 - 4: id1])
                    if 'N' in r:
                        return ['он', 'писали']
                    else:
                        left = id1 - 4
                        break
        if id1 - 3 >= 0 and left == -1 and not (',' in l[id1 - 3: id1]): 
            for i in resl3:
                if i[0] == part:
                    r = check(l[id1 - 3: id1])
                    if 'N' in r:
                        return ['он', 'писали']
                    else:
                        left = id1 - 3
                        break
        if id1 - 2 >= 0 and left == -1 and not (',' in l[id1 - 3: id1]): 
            for i in resl2:
                if i[0] == part:
                    r = check(l[id1 - 2: id1])
                    if 'N' in r:
                        return ['он', 'писали']
                    else:
                        left = id1 - 2
                        break
        if id1 - 1 >= 0 and left == -1:
            for i in resl1:
                if i[0] == part:
                    left = id1 - 1
                    break
        print(left)
        print(l, "!!!!!!!!!!!!!!!!!!")
        if left != -1:
            print("Инфинитив")
            while ',' in l[1: left]:
                if l[left - 1] == ',' and l[left - 3] == ',':
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 2])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '6':
                            left = left - 2
                            break
                elif l[left - 1] == ',' and l[left - 4] == ',':
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 3])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '6':
                            r = check(l[left - 3:left - 1])
                            print("R", r)
                            if 'N' in r:
                                return ['он', 'писали']
                            elif 'Y' in r:
                                left = left - 3
                                break
                elif l[left - 1] == ',' and l[left - 5] == ',':
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 4])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '6':
                            r = check(l[left - 4:left - 1])
                            print("R", r)
                            if 'N' in r:
                                return ['он', 'писали']
                            elif 'Y' in r:
                                left = left - 4
                                break
                elif l[left - 1] == ',' and l[left - 6] == ',':
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 5])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '6':
                            r = check(l[left - 5:left - 1])
                            print("R", r)
                            if 'N' in r:
                                return ['он', 'писали']
                            elif 'Y' in r:
                                left = left - 5
                                break
                elif l[left - 1] == ',' and left - 2 >= 0:
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 2])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '6':
                            left = left - 2
                            print(i[0])
                            break
                        elif l[left - 1] == ',' and left - 3 >= 0:
                            cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 3])
                            res1 = cur.fetchall()
                            res1 = list(set(res1))
                            for i in res1:
                                if i[0] == '6':
                                    r = check(l[left - 3:left - 1])
                                    print("R!", r)
                                    if 'N' in r:
                                        return ['он', 'писали']
                                    elif 'Y' in r:
                                        left = left - 3
                                        print("OK!!!")
                                        break
                                elif l[left - 1] == ',' and left - 4 >= 0:
                                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 4])
                                    res1 = cur.fetchall()
                                    res1 = list(set(res1))
                                    for i in res1:
                                        if i[0] == '6':
                                            r = check(l[left - 4:left - 1])
                                            print("R!!!", r)
                                            if 'N' in r:
                                                return ['он', 'писали']
                                            elif 'Y' in r:
                                                left = left - 4
                                                print("OK!!!!!")
                                                break
                                        elif l[left - 1] == ',' and left - 5 >= 0:
                                            cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 5])
                                            res1 = cur.fetchall()
                                            res1 = list(set(res1))
                                            for i in res1:
                                                if i[0] == '6':
                                                    r = check(l[left - 5:left - 1])
                                                    print("R!!!", r)
                                                    if 'N' in r:
                                                        return ['он', 'писали']
                                                    elif 'Y' in r:
                                                        left = left - 5
                                                        print("OK!!!!!")
                                                        break
        print(l)
        l = l[:left] + ['учить'] + l[right + 1:]
    elif part == '5':
        print("verb")
        if id1 - 6 >= 0 and left == -1 and not(',' in l[id1 - 5: id1]): # он мечтал поехать изучать основы теории кодирования и бегал
            sng1 = []
            r = []
            for i in resl6:
                if i[0] == part:
                    sng1 += list(i[1])
                    r += check(l[id1 - 6: id1])
            if len(sng1) > 0:
                if sng in sng1 and 'Y' in r:
                    left = id1 - 6
                    print(left, right, "границы")
                else:
                    return ['он', 'писали']
        if id1 - 5 >= 0 and left == -1 and not(',' in l[id1 - 5: id1]):
            sng1 = []
            r = []
            for i in resl5:
                if i[0] == part:
                    sng1 += list(i[1])
                    r += check(l[id1 - 5: id1])
            if len(sng1) > 0:
                if sng in sng1 and 'Y' in r:
                    left = id1 - 5
                    print(left, right, "границы")
                else:
                    return ['он', 'писали']
        if id1 - 4 >= 0 and left == -1 and not(',' in l[id1 - 4: id1]): # я пойду куплю икру нерки и умру
            sng1 = []
            r = []
            for i in resl4:
                if i[0] == part:
                    sng1 += list(i[1])
                    r += check(l[id1 - 4: id1])
            if len(sng1) > 0:
                if sng in sng1 and 'Y' in r:
                    left = id1 - 4
                    print(left, right, "границы")
                else:
                    return ['он', 'писали']
        if id1 - 3 >= 0 and left == -1 and not(',' in l[id1 - 3: id1]):
            sng1 = []
            r = []
            for i in resl3:
                if i[0] == part:
                    sng1 += list(i[1])
                    r += check(l[id1 - 3: id1])
            if len(sng1) > 0:
                if sng in sng1 and 'Y' in r:
                    left = id1 - 3
                    print(left, right, "границы")
                else:
                    return ['он', 'писали']
        if id1 - 2 >= 0 and left == -1 and not(',' in l[id1 - 2: id1]): # защита от пойду схожу
            sng1 = []
            r = []
            for i in resl2:
                if i[0] == part:
                    sng1 += list(i[1])
                    r += check(l[id1 - 2: id1])
            if len(sng1) > 0:
                if sng in sng1 and 'Y' in r:
                    left = id1 - 2
                    print(left, right, "границы")
                else:
                    return ['он', 'писали']
        if id1 - 1 >= 0 and left == -1:
            sng1 = []
            for i in  resl1:
                if i[0] == part:
                    if i[1] == sng:
                        sng1 += list(sng)
            if sng in sng1:
                left = id1 - 1
                print(left, right, "границы")
            else:
                return ['он', 'писали']
        print("пока всё ок")
        if left != -1:
            print("Личный глагол")
            while ',' in l[1: left]:
                if l[left - 1] == ',' and l[left - 3] == ',':
                    print("ОНО работает!")
                    sng1 = []
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 2])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '5':
                            sng1 += list(i[1])
                    if sng in sng1:
                        left = left - 2
                        print(left, right, "границы")
                    else:
                        return ['он', 'писали']
                elif l[left - 1] == ',' and l[left - 4] == ',':
                    print("ОНО работает!!")
                    sng1 = []
                    r = []
                    for i in resl3:
                        if i[0] == part:
                            sng1 += list(i[1])
                            r += check(l[left - 3: left - 1])
                    if len(sng1) > 0:
                        if sng in sng1 and 'Y' in r:
                            left = left - 3
                            print(left, right, "границы")
                        else:
                            return ['он', 'писали']
                elif l[left - 1] == ',' and left - 2 >= 0:
                    sng1 = []
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 2])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == '5':
                            sng1 += list(i[1])
                    if sng in sng1:
                        left = left - 2
                        print(left, right, "границы")
                    else:
                        return ['он', 'писали']
        """
        if left != -1:
            while ',' in l[left - 4: left]:
                if id1 - 1 >= 0 and left == -1:
                    sng1 = []
                    for i in resl1:
                        if i[0] == part:
                            if i[1] == sng:
                                sng1 += list(sng)
                                print(sng1, "число!")
                    if sng in sng1:
                        left = id1 - 1
                    else:
                        return ['он', 'писали']
                    print(left, right, "границы")
                elif l[left - 1] == ',' and left - 2 >= 0:
                    sng1 = []
                    cur.execute("select pos, singular, cow from words where word = '%s'" % l[left - 2])
                    res1 = cur.fetchall()
                    res1 = list(set(res1))
                    for i in res1:
                        if i[0] == part:
                            if i[1] == sng:
                                sng1 += list(sng)
                    if sng in sng1:
                        left = left - 2
                    else:
                        return ['он', 'писали']
                    print(left, right, "границы")"""
        if sng == 'Y':
            l = l[:left] + ['учил'] + l[right + 1:]
        elif sng == 'N':
            l = l[:left] + ['учили'] + l[right + 1:]
    return l

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