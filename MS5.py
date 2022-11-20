import math
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import scipy.stats as sps

def arrN(X, a, sigma):
    arr = [sps.norm.pdf(x, a, sigma) for x in X]
    return arr

n = 120
alpha = 0.1
a0 = -3.7
a1 = -3.4
sigma0 = 1.3
sigma1 = 1.3
eps = 0.1

X = [-7.123, -4.539,-3.242,	-3.961,	-2.389,	-4.626,	-2.834,	-4.116,	-5.099,	-4.758,
-0.772,	-4.916,	-6.343,	-3.405,	-3.191,	-4.663,	-3.648,	-5.396,	-2.56,	-3.44,
-2.114,	-1.454,	-3.381,	-3.614,	-2.192,	-2.575,	-0.229,	-3.16,	-4.249,	-2.306,
-3.88,	-2.948,	-6.348,	-4.214,	-3.233,	-2.318,	-3.545,	-2.714,	-3.627,	-2.712,
-3.199,	-2.746,	-3.281,	-4.736,	-3.726,	-3.448,	-2.685,	-4.65,	-3.524,	-2.872,
-4.757,	-4.788,	-2.895,	-3.722,	-1.3,	-4.727,	-2.394,	-4.548,	-2.414,	-4.715,
-2.757,	-4.201,	-2.931,	-2.794,	-4.892,	-2.333,	-3.449,	-3.723,	-1.534,	-3.351,
-3.585,	-2.272,	-3.632,	-0.957,	-2.731,	-4.527,	-2.309,	-3.497,	-5.803,	-3.28,
-3.406,	-2.292,	-3.013,	-2.296,	-4.972,	-4.081,	-4.178,	-4.795,	-2.333,	-3.195,
-4.299,	-7.033,	-2.463,	-4.465,	-3.34,	-4.948,	-2.682,	-3.369,	-3.691,	-2.884,
-3.691,	-3.264,	-3.106,	-3.488,	-2.885,	-4.554,	-4.606,	-3.628,	-5.055,	-5.077,
-1.716,	-1.998,	-4.397,	-3.771,	-3.108,	-3.646,	-3.203,	-2.231,	-3.118,	-3.301] 

m = min(X)
M = max(X)
print("Крайние члены вариационного ряда: min(X) = %.5f, max(X) = %.5f" % (m, M))
w = M - m
print("Размах выборки составляет w = %.5f" % w)

l = 1 + math.trunc(math.log2(n))
h = w / l
print("Количество интервалов группировки l: %d" % l)
print("Интервальный шаг h = %.5f" % h)

I = [m + i * h for i in range(l + 1)]

hist = np.histogram(X, l)
values = [0.5 * (hist[1][i] + hist[1][i + 1]) for i in range(l)]

freq = [hist[0][i] for i in range(l)]

relfreq = [freq[i] / n for i in range(l)]

density = [relfreq[i] / h for i in range(l)]

print()

print("Интервал:", end = " " * 24)
for i in range(l):
    print('|', str("[%.5f; %.5f)" % (I[i], I[i + 1])), '|', sep = '', end = ' ' * 2)

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

seaborn.set_style("whitegrid")

x = np.linspace(m, M, 1024)
plt.bar(values, density, width=h, color="navy")
plt.xlabel("int")
plt.ylabel("p^r")
plt.show()

average = np.mean(X)
s2 = np.var(X)
print("Выборочное среднее: %.5f" % average)
print("Квадрат среднеквадратичного отклонения: %.5f" % s2)
print()

print("Критерий S2")
C2 = a0 + sps.t.ppf(1 - alpha, n - 1) * np.sqrt(s2 / n)
print("C2 = %.5f" % C2)
if (average >= C2):
    print("Отвергаем гипотезу H0 в пользу гипотезы H2")
else:
    print("Принимаем гипотезу H0")
print()

print("Критерий S3")
C3 = sigma0 ** 2 / (n - 1) * sps.chi.ppf(alpha, n - 1)
print("C3 = %.5f" % C3)
if (s2 < C3):
    print("Отвергаем гипотезу H01 в пользу гипотезы H3")
else:
    print("Принимаем гипотезу H01")
print()

print("Критерий S1")
C1 = a0 + sigma1 * sps.norm.ppf(1 - alpha) / np.sqrt(n)
print("C1 = %.5f" % C1)
if (average >= C1):
    print("Отвергаем гипотезу H0 в пользу гипотезы H1")
else:
    print("Принимаем гипотезу H0")
print()

beta = sps.norm.cdf((C1 - a1) / sigma1 * np.sqrt(n), 0, 1)
print("beta = %.5f" % beta)

a12 = C1 - sps.norm.ppf(eps) * sigma1 / np.sqrt(n)
print("a12 = %.5f" % a12)

x = np.linspace(m, M, 1024)
plt.bar(values, density, width=h, color = "gray")
plt.plot(x, arrN(x, a0, sigma1), color = "red", linestyle = "dotted")
plt.plot(x, arrN(x, a1, sigma1), color = "navy", linewidth = 2.0)
plt.xlabel("int")
plt.ylabel("p^r")
plt.show()