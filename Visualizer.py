import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm


d0 = 120
d12 = 120

data = np.loadtxt("Histograms/EGamma_661/d0_"+str(d0)+"/d12_"+str(d12))
print(len(data),len(data[0]))
plt.figure(1,figsize=(5,4))
plt.clf()
plt.imshow(data,cmap = plt.cm.jet,origin="lower",extent=[0,180,0,700],aspect="auto",interpolation="None",norm=LogNorm())


data2 = np.loadtxt("ComptonHists/ComptonHist_661")

print(len(data2),len(data2[0]))

plt.figure(2, figsize=(5, 4))
plt.clf()
plt.imshow(data2, cmap=plt.cm.jet, origin="lower",
           extent=[-1, 1, 0, 700], aspect="auto")

data3 = np.loadtxt("d0_0/d12_0")

print(len(data3), len(data3[0]))

from matplotlib.colors import LogNorm

plt.figure(3, figsize=(5, 4))
plt.clf()
plt.imshow(data3, cmap=plt.cm.jet, origin="lower",
           extent=[-1, 1, 0, 180], aspect="auto")


xbins = np.array([i for i in range(181)])

dataRange = np.loadtxt("Histograms/EGamma_661/d0_"+str(d0)+"/d12_"+str(d12)+"_Ranges")

norm = 0
for i in range(len(data)):
    norm = 0
    for j in range(len(data[0])):
        norm += data[i,j]
    if norm > 0:
        data[i,:] /= norm

colors = plt.cm.jet(np.linspace(0,1,len(data)))

plt.figure(4, figsize=(5, 4))
plt.clf()

for i in range(len(data)):
    if i % 10 != 0:
        continue
    plt.plot(xbins,data[i,:],color=colors[i],ls=':',marker='o',ms=2,label=str(i*4))
    plt.axvline(dataRange[i,0],color=colors[i],ls='-',lw=1.5,label=str(i*4))
    plt.axvline(dataRange[i,1],color=colors[i],ls='-',lw=1.5)
    print(i*4,dataRange[i,0],dataRange[i,1])

plt.legend(loc=1)