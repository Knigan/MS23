import math
import random
import scipy
import numpy
import matplotlib.pyplot as plt

n = 120

def p(x):
    if x > 0:
        return 1/x * math.sqrt(2/math.pi) * math.exp(-2*(math.log(x) - 1) ** 2)
    else:
        return 0

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
    return Femp(X, z) - math.exp(-2 * n * eps * eps)

def arrL(X, array, eps):
    arr = []
    for z in array:
        arr.append(L(X, z, eps))
    return arr

def R(X, z, eps):
    return Femp(X, z) + math.exp(-2 * n * eps * eps)

def arrR(X, array, eps):
    arr = []
    for z in array:
        arr.append(R(X, z, eps))
    return arr

def rounding(X, num):
    arr = []
    for k in X:
        arr.append(round(k, num))
    return arr

def Hvecs(X, Y, width, M, m):
    arrX = X
    arrY = Y
    for i in range(len(X)):
        x = X[i]
        if not(x + width in X) and x < M:
            arrX.append(x + width)
            arrY.append(Y[i])
        #if not(x - width in X) and x > m:
        #    arrX.append(x - width)
        #    arrY.append(Y[i])
    return (arrX, arrY)

def fitting(X, Y, width, M, m, n):
    X1 = X
    Y1 = Y
    for i in range(n):
        arrays = Hvecs(X1, Y1, width, M, m)
        X1 = arrays[0]
        Y1 = arrays[1]
    return (X1, Y1)


Y = randvec()
arrprint("Y^T = ", Y)

X = Xvec(Y)
arrprint("X^T = ", X)

M = math.exp(1.125)
av = sum(X) / n
print("M = exp(9/8) = %.5f" % M)
print("Average x = %.5f" % av)
print("Comparison: M - average = %.5f is small" % (M - av))

D = math.exp(2.5) - math.exp(2.25)
S = S2(X)
print("D = exp(5/2) - exp(9/4) = %.5f" % D)
print("S^2 = %.5f" % S)
print("Comparison: D / S^2 = %.5f is small" % (D / S))

w = 1
arrays = fitting(rounding(X, 1), rounding(Y, 1), w, max(X), min(X), 1)
X1 = arrays[0]
Y1 = arrays[1]

plt.hist(Y, bins = math.trunc(math.log(n, 2)), linewidth = 0.5, edgecolor = "white")
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