import math
import numpy as np
import seaborn
import matplotlib.pyplot as plt

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

def D1(I, F):
    Sets = [(I[i], I[i + 1], F[i]) for i in range(len(F))]
    return 1 / n * max([abs(Sets[j][2] - n * SetP(Sets[j][0], Sets[j][1])) for j in range(len(Sets))])

l = 1 + math.trunc(math.log2(n))
print("Количество интервалов группировки l: %d" % l)

h = 1 / l
print("Интервальный шаг h = %.5f" % h)

Int = [i * h for i in range(l + 1)]


def Dm(sample):
    X = sample()

    hist = np.histogram(X, l)

    freq = [hist[0][i] for i in range(l)]

    return D1(Int, freq)

def quantile(arr, alpha):
    return arr[math.floor((1 - alpha) * m) - 1]

def Dmprint(sample):
    X = sample()
    print()
    print(X[:10])

    minX = min(X)
    M = max(X)
    print("Крайние члены вариационного ряда: min(X) = %.5f, max(X) = %.5f" % (minX, M))
    w = M - minX
    print("Размах выборки составляет w = %.5f" % w)

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
    print()

    print("D = %.5f" % D1(Int, freq))
    print()

    return D1(Int, freq)


Dmprint(sample2)
print()

th = [SetP(i / l, (i + 1) / l) for i in range(l)]
print("Теоретические вероятности: ", th)

nth = [n * th[i] for i in range(l)]
print("n*p_j: ", nth)

print()

D = [Dm(sample2) for i in range(m)]
D.sort()

print("Квантиль уровня 0.1 равна %.10f" % quantile(D, 0.1))
print("Квантиль уровня 0.05 равна %.10f" % quantile(D, 0.05))
print("Квантиль уровня 0.01 равна %.10f" % quantile(D, 0.01))

print()

print()

print("D (A = 0) = %.5f" % Dmprint(sample0))
print("D (A = 1) = %.5f" % Dmprint(sample1))

print()
print(D[:10])
print(D[-10:])

seaborn.set_style("whitegrid")

l1 = 1 + math.trunc(math.log2(m))
print("Количество интервалов группировки l: %d" % l1)

h1 = 1 / l1
print("Интервальный шаг h = %.5f" % h1)

Int1 = [i * h1 for i in range(l1 + 1)] 

IntD = [0.5 * (Int1[i] + Int1[i + 1]) for i in range(l1)]

hist = np.histogram(D, l1)

freq = [hist[0][i] for i in range(l1)]

relfreq = [freq[i] / m for i in range(l1)]

density = [relfreq[i] / h1 for i in range(l1)]

plt.bar(IntD, relfreq, width = h1, color="navy")
plt.xlabel("int")
plt.ylabel("Относительные частоты")
plt.show()

plt.bar(IntD, density, width = h1, color="navy")
plt.xlabel("int")
plt.ylabel("Плотность относительных частот")
plt.show()
