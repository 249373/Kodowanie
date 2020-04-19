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


def loadDataTxt(path):
    words_list = []
    dane_txt = open(path, mode="r+")
    for line in dane_txt:
        word_list = list(line)
        word_list.pop()
        for i in range(len(word_list)):
            word_list[i] = int(word_list[i])
        word_list.reverse()
        words_list.append(word_list)
    return words_list


# pamiętaj o dobrym pobieraniu potegi kolejnosc potęg

def enter_word(word):
    word_list = []
    word_list = list(word)
    for i in range(len(word_list)):
        word_list[i] = int(word_list[i])
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
            print("x^" + str(i), end='', )
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
        print("Poprawnie odebrany sygnał")
        for i in range(9, 16):
            h.append(cx[i])
    if haming_distance(calculateSyndrom(cx)) > 1:
        print("Błąd przekraczający zdolność korekcyjną")
    if haming_distance(calculateSyndrom(cx)) == 1:
        cx = recode(cx)
        for i in range(len(cx) - len(polynomialG) + 1):
            h.append(cx[i + len(polynomialG) - 1])
        print("Blad informacji naprawiony metoda polowania na bledy")
    return h


def decode_list():
    try:
        for word_list in loadDataTxt("c(x).txt"):
            print("c(x)=", end='')
            displayPolynomial(word_list)
            h = decode(word_list)
            print("h(x)=", end='')
            displayPolynomial(h)
            print("")
    except IndexError:
        print("Błąd pobrania wyrazu!!!!")
        print("Na końcu KARZDEGO wyrazu w pliku tekstowym należy umieścić enter (również przy ostatnim)")
    return


def encode_list():
    try:
        for word_list in loadDataTxt("h(x).txt"):
            print("h(x)=", end='')
            displayPolynomial(word_list)
            c = encode(word_list)
            print("c(x)=", end='')
            displayPolynomial(c)
            print()
    except IndexError:
        print("BłĄD POBRANIA WYRAZU!!!!")
        print("Na końcu KARZDEGO wyrazu w pliku tekstowym należy umieścić enter (również przy ostatnim)")

def recode(cx):
    for i in range(len(cx)):
        cx.append(cx[0])
        cx.pop(0)
        if remainder_by_G(cx) == 1:
            cx = remainder_by_G(cx) + cx
    return cx


print("Jaka operacje wykonac? (podaj numet i zatwierdź enterem)")
print("1. Koduj jeden wyraz wpisując go w wiersz polecen")
print("2. Dekoduj jeden wyraz wpisując go w wiersz polecen")
print("3. Koduj wyrazy z pliku h(x).txt")
print("4. Dekoduj wyrazy z pliku c(x).txt")

switch = input()

if switch == "1":
    word = input("Podaj 7 liczb wyrazu zaczynajac od najwyższej potęgi x^6 i naciśnij enter.")
    print("h(x)=", end='')
    displayPolynomial(enter_word(word))
    cx = encode(enter_word(word))
    if cx != "":
        print("c(x)=", end='')
    displayPolynomial(cx)
    input("")

if switch == "2":
    word = input("Podaj 16 liczb wyrazu zaczynajac od najwyższej potęgi x^15 i naciśnij enter.")
    print("c(x)=", end='')
    displayPolynomial(enter_word(word))
    hx = decode(enter_word(word))
    if hx != "":
        print("h(x)=", end='')
    displayPolynomial(hx)
    input("")

if switch == "3":
    try:
        encode_list()
        input("")
    except FileNotFoundError:
        input("Brak pliku h(x).txt")
if switch == "4":
    try:
        decode_list()
        input("")
    except FileNotFoundError:
        input("Brak pliku c(x).txt")


