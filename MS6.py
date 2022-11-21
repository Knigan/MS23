import math
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import scipy.stats as sps

n = 120
a0 = -3.7
a1 = -3.4
sigma1 = 1.3
alpha = 0.1
C1 = a0 + sigma1 * sps.norm.ppf(1 - alpha) / np.sqrt(n)
beta = sps.norm.cdf((C1 - a1) / sigma1 * np.sqrt(n), 0, 1)
A = (1 - beta) / alpha
B = beta / (1 - alpha)

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

def Z(j):
    return math.exp(j * (a0 * a0 - a1 * a1) / (2 * sigma1 * sigma1) 
    + (a1 - a0) / (sigma1 * sigma1) * sum(X[:j]))

print("A = %.5f" % A)
print("B = %.5f" % B)
print("C1 = %.5f" % C1)

seaborn.set_style("whitegrid")
j = np.arange(0, n + 1, 1)
plt.plot(j, [Z(i) for i in j], linewidth = 2.0)
plt.plot(j, 0 * j + A, linewidth = 2.0, color = "red")
plt.plot(j, 0 * j + B, linewidth = 2.0, color = "green")
plt.xlabel("j")
plt.ylabel("Green: B\nRed: A")
plt.show()

M0 = - (a1 - a0) * (a1 - a0) / (2 * sigma1 * sigma1)
print("M0 = %.6f" % M0)

Ma0 = (alpha * math.log(A) + (1 - alpha) * math.log(B)) / M0
print("Ma0 = %.3f" % Ma0)

M1 = (a1 - a0) * (a1 - a0) / (2 * sigma1 * sigma1)
print("M1 = %.6f" % M1)

Ma1 = (beta * math.log(B) + (1 - beta) * math.log(A)) / M1
print("Ma1 = %.3f" % Ma1)

C = math.exp(n * (a1 - a0) / (sigma1 * sigma1) * (C1 - 0.5 * (a0 + a1)))
print("C = %.5f" % C)

plt.plot(j, [Z(i) for i in j], linewidth = 2.0)
plt.plot(j, 0 * j + A, linewidth = 2.0, color = "red")
plt.plot(j, 0 * j + B, linewidth = 2.0, color = "green")
plt.plot(j, 0 * j + C, linewidth = 2.0, color = "blue")
plt.xlabel("j")
plt.ylabel("Green: B\nRed: A\nBlue: C")
plt.show()

print("Z(n) = %.5f" % Z(n))