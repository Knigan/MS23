import math
import random
import scipy
import numpy
import matplotlib.pyplot as plt
import seaborn

n = 120

def p(x):
    if x > 0:
        return 1/x * math.sqrt(2/math.pi) * math.exp(-2*(math.log(x) - 1) ** 2)
    else:
        return 0

def arrP(array):
    arr = []
    for x in array:
        arr.append(p(x))
    return arr

def F(x):
    if (x > 0):
        return 0.5 * (math.erf((math.log(x) - 1) * math.sqrt(2)) + 1)
    else:
        return 0

def arrF(array):
    arr = []
    for x in array:
        arr.append(F(x))
    return arr

def inv(y):
    return math.exp(1 + math.sqrt(0.5) * scipy.special.erfinv(2 * y - 1))

def randvec():
    y = []
    for i in range(n):
        y.append(random.random())
        
    return y

def Xvec(y):
    X = []
    for k in y:
        X.append(inv(k))

    return X

def S2(X):
    S = 0
    av = sum(X) / n
    for k in X:
        S += (k - av) ** 2
    return S / (n - 1)

def ind(z):
    if (z > 0):
        return 1
    else:
        return 0

def Femp(X, z):
    S = 0
    for k in X:
        S += ind(z - k)
    return S / n

def arrFemp(X, array):
    arr = []
    for k in array:
        arr.append(Femp(X, k))
    return arr

def arrprint(message, arr, precision = 5):
    if (precision >= 8):
        N = 8
    else:
        N = 32 - 3 * precision
    print(message, "[", sep = '', end = '')
    for i in range(len(arr)):
        if i == len(arr) - 1:
            print("{:.{}f}".format(arr[i], precision), end = ']\n')
        else:
            if (i == 0 or i % N != 0):
                print("{:.{}f}".format(arr[i], precision), end = ', ')
            else:
                print("{:.{}f}".format(arr[i], precision), end = ',\n')
    print()

def L(X, z, eps):
    num = Femp(X, z) - math.exp(-2 * n * eps * eps)
    if num > 0:
        if num < 1:
            return num
        else:
            return 1
    else:
        return 0

def arrL(X, array, eps):
    arr = []
    for z in array:
        arr.append(L(X, z, eps))
    return arr

def R(X, z, eps):
    num = Femp(X, z) + math.exp(-2 * n * eps * eps)
    if num > 0:
        if num < 1:
            return num
        else:
            return 1
    else:
        return 0

def arrR(X, array, eps):
    arr = []
    for z in array:
        arr.append(R(X, z, eps))
    return arr

while (True):
    Y = randvec()
    arrprint("Y^T = ", Y)

    X = Xvec(Y)
    arrprint("X^T = ", X)

    M = math.exp(1.125)
    av = sum(X) / n
    
    if abs(M - av) > 0.01:
        continue
    
    D = math.exp(2.5) - math.exp(2.25)
    S = S2(X)

    if abs(D / S - 1) > 0.05:
        continue

    print("M = exp(9/8) = %.5f" % M)
    print("Average x = %.5f" % av)
    print("Comparison: M - average = %.5f is small" % (M - av))

    print("D = exp(5/2) - exp(9/4) = %.5f" % D)
    print("S^2 = %.5f" % S)
    print("Comparison: D / S^2 = %.5f is close to 1" % (D / S))

    m = min(X)
    M = max(X)

    print("Крайние члены вариационного ряда и размах выборки: %f, %f, %f" % (m, M, M - m))

    l = math.trunc(1 + math.log2(n))
    h = (max(X) - min(X)) / l
    print("Число интервалов и шаг интервалов группировки: %d, %f" % (l, h))

    hist = numpy.histogram(X, l)
    values = []
    for i in range(l):
        values.append(0.5 * (hist[1][i] + hist[1][i + 1]))

    freq = []
    for i in range(l):
        freq.append(hist[0][i])

    relfreq = []
    for i in range(l):
        relfreq.append(int(hist[0][i]) / n)

    f2 = []
    for i in range(l):
        f2.append(relfreq[i] / h)

    Int = values
    int1 = []
    for i in Int:
        int1.append(i - 0.5 * h)
    int1.append(M)

    print('Интервал:', end = ' ' * 14)

    for i in range(l):
        print('|', str("[%.4f; %.4f)" % (int1[i], int1[i + 1])), '|', sep = '', end = ' ' * 2)

    print()

    print('Середина интервала:', end = ' ' * 4)

    for i in range(l):
        print('|', str("%.4f" % (0.5 * (int1[i] + int1[i + 1]))).center(6), '|', end = ' ' * 10)

    print()

    print('Частоты:', end = ' ' * 15)

    for i in range(l):
        print('|', str(freq[i]).center(6), '|', end = ' ' * 10)

    print()

    print('Относительные частоты:', end = ' ')

    for i in range(l):
        print('|', str("%.4f" % relfreq[i]).center(6), '|', end = ' ' * 10)

    print()

    break

plt.figure(figsize=(10,6))
seaborn.set_style("whitegrid")

x = numpy.linspace(0, math.ceil(max(hist[1])) + 1, 100)
plt.bar(values, f2, width=h, color="grey")
plt.plot(x, arrP(x), linewidth = 2.0, color="red")
plt.show()

plt.bar(values, f2, width=h, color="grey")
plt.plot(values, f2, color="black")
plt.show()

x = numpy.linspace(-1, 12, 100)
plt.plot(x, arrF(x), linewidth = 2.0)
plt.plot(x, arrFemp(X, x), linewidth = 2.0)

eps = 0.1

plt.plot(x, arrL(X, x, eps), linewidth = 2.0)
plt.plot(x, arrR(X, x, eps), linewidth = 2.0)
plt.xlabel("z")
plt.ylabel("Blue: F(z)\nOrange: Femp(z)\nGreen: L(z)\nRed: R(z)")
plt.show()