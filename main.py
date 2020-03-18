import os
import sys

polynomialG = [1, 1, 0, 0, 0, 0, 0, 0, 1, 1]

Ht = [[1, 1, 0, 0, 0, 0, 0, 0, 1],
      [1, 0, 1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 1, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 0, 1, 0, 0, 1],
      [1, 0, 0, 0, 0, 0, 1, 0, 1],
      [1, 0, 0, 0, 0, 0, 0, 1, 1],
      [1, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 1]]

dane = []


def loadDataTxt():
    words_list = []
    dane_txt = open("dane.txt", mode="r+")
    for word in dane_txt:
        if 1:
            word_list = []
            for i in range(16):
                word_list.append(int(word[i]))
            word_list.reverse()
            words_list.append(word_list)
        else:
            print("Blad danych")
            print("Niepoprawnie zapisany wiersz numer {}".format(len(dane)))

    return words_list


# pamiętaj o dobrym pobieraniu potegi kolejnosc potęg

def enterA():
    word = input("Proszę wpisać wyraz zaczynająć od najwyższej potęgi x^7 i oddzielajac spacja np.1 1 0 1 0 1 1")
    word_list = []
    for i in range(len(word)):
        word_list.append(int(word[i]))
    word_list.reverse()

    return word_list


def splitString(napis, a=None):
    if a is None:
        a = []
    tablica = napis.split()
    for cyfra in tablica:
        if cyfra == "1" or cyfra == "0":
            a.append(int(cyfra))
        else:
            return "NO BINARY"
    a.reverse()
    return a


def displayPolynomial(p):
    needPlus = False
    for i in range(len(p) - 1, -1, -1):
        if p[i] != 0:
            if needPlus == True:
                print(" + ", end='')
            print("[" + str(p[i]) + "]x^" + str(i), end='', )
            needPlus = True
    print()


def calculateSyndrom(__c):
    __S = []
    __c.reverse()
    for j in range(len(Ht[0])):
        __S.append(0)
    for j in range(len(Ht[0])):
        for i in range(len(Ht)):
            __S[j] = (__S[j] + (__c[i] * Ht[i][j])) % 2
    __S.reverse()
    __c.reverse()

    return __S


def addPolynomaial(a, b):
    c = []
    if len(a) == len(b):
        for i in range(len(a)):
            c[i] = a[i] + b[i]
    return c


def slideA(a):
    lenght = len(a)
    a.append(0)
    a.append(0)
    for i in range(lenght):  # przesuwamy wielomian informacyjny
        a.append(a[i])
        a[i] = 0
    return a


def slide_tmp(tmp):
    if tmp[len(tmp) - 1] == 0:
        for i in range(len(tmp) - 1, 0, -1):
            tmp[i] = tmp[i - 1]
        tmp[0] = 0
    else:
        print("Slide TMP niewykonalny bo największa potęga zajęta")
    return tmp


def remainder_by_G(__a, tmp=None):
    if tmp is None:
        tmp = []
    for i in range(len(polynomialG)):
        tmp.append(__a[i + 6])
    for i in range(len(__a) - len(polynomialG), -1, -1):
        if tmp[len(tmp) - 1] == 0:
            if i != 0 or 1 != len(__a) - len(polynomialG):
                tmp = slide_tmp(tmp)
                tmp[0] = __a[i]
            continue
        for j in range(len(polynomialG)):
            tmp[j] = (tmp[j] + polynomialG[j]) % 2
        tmp = slide_tmp(tmp)
    tmp.pop(0)
    return tmp


def encode(h):
    a = h[:]
    cx = slideA(a)
    tmp = remainder_by_G(cx)
    for i in range(len(tmp)):
        cx[i] = tmp[i]
    return cx


def haming_distance(s):
    sum = 0
    for number in s:
        if number == 1:
            sum += 1
    return sum


def decode(cx):
    h = []
    if haming_distance(calculateSyndrom(cx)) == 0:
        for i in range(len(cx) - len(polynomialG) + 1):
            h.append(cx[i + len(polynomialG) - 1])
    if haming_distance(calculateSyndrom(cx)) > 1:
        "Błąd przekraczający zdolność korekcyjną"
    if haming_distance(calculateSyndrom(cx)) == 1:
        print("polujmy na błedy")
    return h

def decode_list():
    for word_list in loadDataTxt():
        print(decode(word_list))
    return



# był problem z liczeniem reszty z dzielenia, bo zajmwoała 10 miejsc a powinna 9


# b = [1,0,1,0,1,0,1]
# c = [1,1,0,0,1,0,1]
# d = [1,0,1,1,0,0,0]
# e = [1,0,0,0,1,0,1]
# kartka = [1,0,0,0,1,0,0]
#
# print(encode(b))
# print(encode(c))
# print(encode(d))
# print(encode(e))
# print(encode(kartka))


decode_list()
# nawet dziła tylko mało intuicyjnie dla mnie ale tam ma być
#dodajesz wartości błedne na dekoder i on robi tylko spacje




