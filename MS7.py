import math
import numpy as np

n = 100
m = 20000 + 10000000 // n
print("m =", m)

def sample0():
    arr = np.random.rand(n)
    return arr

def sample1():
    arr = np.random.rand(n)
    for i in range(n):
        arr[i] = math.sqrt(arr[i])

    return arr

def sample2():
    arr = np.random.rand(n)
    for i in range(n):
        arr[i] = 1 - math.sqrt(arr[i])

    return arr

def SetP(a, b):
    return (2 * b - b * b) - (2 * a - a * a)

def D1(Int, freq):
    Sets = [(Int[i], Int[i + 1], freq[i]) for i in range(len(freq))]
    return 1 / n * max([abs(Sets[j][2] - n * SetP(Sets[j][0], Sets[j][1])) for j in range(len(Sets))])

def Dm(sample):
    X = sample()

    minX = min(X)
    M = max(X)
    w = M - minX

    l = 1 + math.trunc(math.log2(n))
    h = w / l

    Int = [minX + i * h for i in range(l + 1)]

    hist = np.histogram(X, l)

    freq = [hist[0][i] for i in range(l)]

    return D1(Int, freq)

def quantile(D, alpha):
    return D[math.floor((1 - alpha) * m) - 1]

def Dmprint(sample):
    X = sample()
    print()
    print(X[:10])

    minX = min(X)
    M = max(X)
    print("Крайние члены вариационного ряда: min(X) = %.5f, max(X) = %.5f" % (minX, M))
    w = M - minX
    print("Размах выборки составляет w = %.5f" % w)

    l = 1 + math.trunc(math.log2(n))
    h = w / l
    print("Количество интервалов группировки l: %d" % l)
    print("Интервальный шаг h = %.5f" % h)

    Int = [minX + i * h for i in range(l + 1)]

    hist = np.histogram(X, l)

    freq = [hist[0][i] for i in range(l)]

    relfreq = [freq[i] / n for i in range(l)]

    density = [relfreq[i] / h for i in range(l)]

    print()

    print("Интервал:", end = " " * 24)
    for i in range(l):
        print('|', str("[%.5f; %.5f)" % (Int[i], Int[i + 1])), '|', sep = ' ', end = ' ' * 2)

    print()

    print("Частоты:", end = " " * 25)

    for i in range(l):
        print('|', str(freq[i]).center(18), '|', end = ' ' * 2)

    print()

    print("Относительные частоты:", end = " " * 11)

    for i in range(l):
        print('|', str("%.5f" % relfreq[i]).center(18), '|', end = ' ' * 2)

    print()

    print("Плотность относительной частоты:", end=" ")
    for i in range(l):
        print('|', str("%.5f" % density[i]).center(18), '|', end = " " * 2)

    print()

    print("D = %.5f" % D1(Int, freq))
    print()

    return D1(Int, freq)

Dmprint(sample2)

D = [Dm(sample2) for i in range(m)]
D.sort()

print("Квантиль уровня 0.1 равна %.5f" % quantile(D, 01.1))
print("Квантиль уровня 0.05 равна %.5f" % quantile(D, 0.05))
print("Квантиль уровня 0.01 равна %.5f" % quantile(D, 0.01))

print("D (A = 0) = %.5f" % Dmprint(sample0))
print("D (A = 1) = %.5f" % Dmprint(sample1))

print()
print(D[:10])
print(D[-10:])