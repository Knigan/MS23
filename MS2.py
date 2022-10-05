import math
import random
import matplotlib.pyplot as plt
import numpy

k = 15
p = 0.3
n = 160

def prob():
    arr = []
    for j in range(k + 1):
        P = math.comb(k, j) * p ** j * (1 - p) ** (k - j)
        arr.append(P)
    return arr

def cumprob():
    P = 0
    arr = []
    array = prob()
    for elem in array:
        P += elem
        arr.append(P)
    return arr

def randvec():
    y = []
    for i in range(n):
        y.append(random.random())
        
    return y

def Xvec(y):
    x = []
    u = cumprob()
    for elem in y:
        for i in range(len(u)):
            if elem < u[i]:
                x.append(i)
                break
    return x

def freq(x):
    arr = []
    for i in range(k + 1):
        arr.append(x.count(i))

    return arr

def relfreq(x):
    arr = freq(x)
    for i in range(len(arr)):
        arr[i] /= n
        
    return arr

def cumfreq(x):
    arr = relfreq(x)
    for i in range(1, len(arr)):
        arr[i] += arr[i - 1]

    return arr

def F(z):
    if (z <= 0):
        return 0
    if (z >= k):
        return 1
    
    
    arr = cumprob()
    for i in range(len(arr)):
        if z > i and z <= i + 1:
            return arr[i]

def arrF(array):
    arr = []
    for z in array:
        arr.append(F(z))
    return arr
        

def Fn(x, z):
    if (z <= 0):
        return 0
    if (z > k):
        return 1
    
    arr = cumfreq(x)
    for i in range(len(arr)):
        if z > i and z <= i + 1:
            return arr[i]

def arrFn(x, array):
    arr = []
    for z in array:
        arr.append(Fn(x, z))
    return arr

def arrDiff(x, array):
    arr = []
    for z in array:
        arr.append(F(z) - Fn(x, z))
    return arr

def Dn(x, array):
    M = 0
    for z in array:
        diff = abs(F(z) - Fn(x, z))
        if diff > M:
            M = diff
    return M

def arrprint(message, arr, precision = 8):
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
            

P = prob()
arrprint("P = ", P)

U = cumprob()
arrprint("U = ", U)

Y = randvec()
arrprint("Y^T = ", Y)

X = Xvec(Y)
arrprint("X^T = ", X, 0)

for i in range(k + 1):
    print('|', str(i).center(6), '|', end = ' ' * 4)

print()
Fq = freq(X)

for i in range(k + 1):
    print('|', str(Fq[i]).center(6), '|', end = ' ' * 4)

print()
RF = relfreq(X)

for i in range(k + 1):
    print('|', str("%.4f" % RF[i]).center(6), '|', end = ' ' * 4)

print()
CF = cumfreq(X)

for i in range(k + 1):
    print('|', str("%.4f" % CF[i]).center(6), '|', end = ' ' * 4)

print()

z = numpy.linspace(-1, 16, 1024)

print("Статистика Колмогорова: %.8f" % Dn(X, z))

plt.plot(z, arrF(z), linewidth = 2.0)
plt.plot(z, arrFn(X, z), linewidth = 2.0)
plt.xlabel("z")
plt.ylabel("Blue: F(z)\nOrange: F160(z)")
plt.show()