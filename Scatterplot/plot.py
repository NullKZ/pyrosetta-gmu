import numpy as np
import matplotlib.pyplot as plt
import os
import statistics

protein = "1ail"
x = []
y = []

txts = [x for x in os.listdir() if ((protein in x) and ".txt" in x)]
i=0
for log in txts:
    with open(log, "r") as f:
        x.append([])
        y.append([])
        for line in f:
            tokenized = line.split(' ')
            try:
                if len(tokenized) != 2: continue
                if float(tokenized[0]) > 25: continue
                if float(tokenized[1]) > 1000: continue
                x[i].append(float(tokenized[0]))
                y[i].append(float(tokenized[1]))
            except Exception:
                continue
    i+=1

area = np.pi * 0.1
fig = plt.figure(figsize=(8,6.2))
ax = fig.add_subplot(1,1,1)
major_ticks = np.arange(0, 26, 5)
minor_ticks = np.arange(0, 26, 1)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_xlim(0,25)
ax.grid(which='both', alpha=0.25)

plt.xlabel("RMSD to native")
plt.ylabel("Rosetta score3 Energy")
plt.title(protein+": Algorithm Comparison")
for log in range(i):
    plt.scatter(x[log],y[log], s=area, label=txts[log][len(protein):-len(protein)])
    print(txts[log][4:-4])
    print("Mean RMSD:\t"+str(statistics.mean(x[log])))
    print("Median RMSD:\t"+str(statistics.median(x[log])))
    print("Min RMSD:\t"+str(min(x[log])))
    print("Max RMSD:\t"+str(max(x[log])))
    print("\n")

plt.legend(loc='best')
plt.show()