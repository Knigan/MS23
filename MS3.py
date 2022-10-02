import math
import random
import scipy

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

def inv(y):
    return math.exp(1 + math.sqrt(0.5) * scipy.special.erfinv(2 * y - 1))

def randvec():
    y = []
    for i in range(n):
        y.append(random.random())
        
    return y

def Xvec(y):
    x = []
    for k in y:
        x.append(inv(k))

    return x

def average(x):
    S = 0
    for k in x:
        S += k
    return S / n

def S2(x):
    S = 0
    av = average(x)
    for k in x:
        S += (k - av) ** 2
    return S / (n - 1)

def ind(z):
    if (z > 0):
        return 1
    else:
        return 0

def Femp(x, z):
    S = 0
    for k in x:
        S += ind(z - k)
    return S / n

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

Y = randvec()
arrprint("Y^T = ", Y)

X = Xvec(Y)
arrprint("X^T = ", X)

M = math.exp(1.125)
av = average(X)
print("M = exp(9/8) = %.5f" % M)
print("Average x = %.5f" % av)
print("Comparison: M - average = %.5f is small" % (M - av))

D = math.exp(2.5) - math.exp(2.25)
S = S2(X)
print("D = exp(5/2) - exp(9/4) = %.5f" % D)
print("S^2 = %.5f" % S)
print("Comparison: D / S^2 = %.5f is small" % (D / S))



