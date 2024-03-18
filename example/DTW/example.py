import matplotlib.pyplot as plt
import numpy as np
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis


a = [1, 2, 5, 7, 4, 3, 6, 8, 2, 1]
b = [3, 6, 1, 2, 8, 9, 3, 4, 3, 2, 1, 2]
c = [2, 5, 7, 4, 3, 6, 8, 2, 1, 1]

fig1, ax1 = plt.subplots()
ax1.plot(a)
ax1.plot(b)
fig2, ax2 = plt.subplots()
ax2.plot(a)
ax2.plot(c)

# # plt.show()
# ab = np.zeros((len(b)+1, len(a)+1))
# print(ab.shape)
# for i, num1 in enumerate(b, 1):
#     for j, num2 in enumerate(a, 1):
#         ab[i][j] = (num1 - num2) ** 2
#         ab[i][j] += min(ab[i-1][j], ab[i][j-1], ab[i-1][j-1])

# print(ab)
print(dtw.distance(a, b))
dtwvis.plot_warping(a, b, dtw.warping_path(a, b))
print(dtw.distance(a, c))
dtwvis.plot_warping(a, c, dtw.warping_path(a, c))
plt.show()