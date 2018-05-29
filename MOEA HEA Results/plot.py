import numpy as np
import matplotlib.pyplot as plt
import os
import statistics

x = []
y = []
name = "1bq9HEA.txt"
i=0
with open(name, "r") as f:
    for line in f:
        x.append(i)
        y.append(float(line))
        i+=1

area = np.pi * 0.1
fig = plt.figure(figsize=(8,6.2))
ax = fig.add_subplot(1,1,1)
major_ticks = np.arange(0, 26, 5)
minor_ticks = np.arange(0, 26, 1)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.set_ylim(0,25)
ax.grid(which='both', alpha=0.25)

plt.xlabel("t")
plt.ylabel("RMSD")
plt.title(name[:-4]+" Over Time")

plt.scatter(x,y, s=area)
print("Mean RMSD:\t"+str(statistics.mean(y)))
print("Median RMSD:\t"+str(statistics.median(y)))
print("Min RMSD:\t"+str(min(y)))
print("Max RMSD:\t"+str(max(y)))
print("\n")

plt.legend(loc='best')
plt.show()
