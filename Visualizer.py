import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

from matplotlib.colors import LogNorm

from matplotlib import rc
rc('text', usetex=True)


d0 = 12
d12 = 12

data = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_"+str(d0)+"/d12_"+str(d12))

print(len(data),len(data[0]))
plt.figure(1,figsize=(5,4))
plt.clf()
plt.imshow(data,cmap = plt.cm.jet,origin="lower",extent=[0,180,0,700],aspect="auto",interpolation="None",norm=LogNorm())

"""
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
"""

xbins = np.array([i for i in range(181)])

dataRange = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_"+str(d0)+"/d12_"+str(d12)+"_Ranges")

data2 = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_120/d12_120")
dataRange2 = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_120/d12_120_Ranges")


norm = 0
for i in range(len(data)):
    norm = 0
    for j in range(len(data[0])):
        norm += data[i,j]
    if norm > 0:
        data[i,:] /= norm

for i in range(len(data2)):
    norm = 0
    for j in range(len(data2[0])):
        norm += data2[i,j]
    if norm > 0:
        data2[i,:] /= norm

colors = plt.cm.jet(np.linspace(0,1,len(data)))



iter = 0
colors2 = ["dodgerblue","orange","crimson"]

#plt.figure(4, figsize=(5, 3))
#plt.clf()

fig,ax = plt.subplots(2,figsize=(5,6),sharex=True)


for i in range(len(data)):
    #if i % 30 != 0 or np.sum(data[i,:]) == 0 or i == 0:
    #    continue
    if i*4 == 120 or i*4 == 360 or i*4 == 520:
        ax[0].plot(xbins,data[i,:],color=colors2[iter],ls=':',marker='o',ms=2,label="$E_\\mathrm{dep} = "+str(i*4)+"$ keV")
        ax[0].vlines(dataRange[i,0],0,0.02,color=colors2[iter],linestyles='dotted',lw=1.5)
        ax[0].vlines(dataRange[i,1],0,0.02,color=colors2[iter],linestyles='dotted',lw=1.5)
        ax[1].plot(xbins,data2[i,:],color=colors2[iter],ls=':',marker='o',ms=2,label="$E_\\mathrm{dep} = "+str(i*4)+"$ keV")
        ax[1].vlines(dataRange2[i,0],0,1,color=colors2[iter],linestyles='dotted',lw=1.5)
        ax[1].vlines(dataRange2[i,1],0,1,color=colors2[iter],linestyles='dotted',lw=1.5)
        iter += 1
        print(i*4,dataRange[i,0],dataRange[i,1])
ax[0].tick_params(axis='both', which='major', labelsize=15)
ax[0].tick_params(axis='both', which='minor', labelsize=10) 
ax[1].tick_params(axis='both', which='major', labelsize=15)
ax[1].tick_params(axis='both', which='minor', labelsize=10) 
ax[1].set_xlabel("$\\vartheta$ (deg)",fontsize=17)
ax[0].set_ylabel("$P(E_\\mathrm{dep},\\vartheta)$",fontsize = 17)
ax[1].set_ylabel("$P(E_\\mathrm{dep},\\vartheta)$",fontsize = 17)
ax[0].set_ylim(0,0.0275)
ax[1].set_ylim(0,0.12)
ax[0].text(188,0.0275/2,"$d_{0,1} = d_{1,2} = 12$ mm",rotation=270,size = 14,ha='center', va='center')
ax[1].text(188,0.06,"$d_{0,1} = d_{1,2} = 120$ mm",rotation=270,size = 14,ha='center', va='center')
ax[0].text(160,0.0275*0.8,"(a)",size = 14,ha='center', va='center')
ax[1].text(160,0.12*0.8,"(b)",size = 14,ha='center', va='center')

for i in range(2):
    ax[i].set_xlim(-2,182)
ax[0].legend(loc=9,frameon=False,fontsize=11,ncol=2)
plt.subplots_adjust(hspace=0.05)
plt.savefig("/home/philipp/FirstPaper/EX22.pdf",bbox_inches="tight")
