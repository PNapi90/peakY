import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

from matplotlib.colors import LogNorm

from matplotlib import rc
rc('text', usetex=True)


d0 = 12
d12 = 12

Eg = 661.7
mc2 = 511

def Ecomp(angle):
    cth = np.cos(angle*np.pi/180)
    return Eg*(1-1/(1+Eg/mc2*(1-cth)))

data = np.loadtxt("Histograms/ExpEGamma_661/d0_"+str(d0)+"/d12_"+str(d12))

psi = np.linspace(0,180,1000)
comp = Ecomp(psi)

print(len(data),len(data[0]))
plt.figure(1,figsize=(5,3))
plt.clf()
plt.imshow(data,cmap = plt.cm.jet,origin="lower",extent=[0,180,0,700],aspect="auto",interpolation="None",norm=LogNorm())
plt.plot(psi,comp,color="k",ls='--',lw=1.5)
cbar = plt.colorbar()
cbar.set_label("$ P ( E_{\\text{dep}},\\vartheta)$",rotation=270,fontsize=15)
cbar.ax.get_yaxis().labelpad = 15
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='minor', labelsize=10)
plt.xlabel("$\\vartheta$ (deg)",fontsize=17)
plt.ylabel("$E_{\\mathrm{dep}}$ (keV)",fontsize = 17)



plt.savefig("/home/philipp/FirstPaper/PEdepTh_AgainExp.pdf",bbox_inches="tight")

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
#/Histograms/ExpEGamma_661
#dataRange = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_"+str(d0)+"/d12_"+str(d12)+"_Ranges")
dataRange = np.loadtxt("Histograms/ExpEGamma_661/d0_"+str(d0)+"/d12_"+str(d12)+"_Ranges")

#data2 = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_120/d12_120")
#dataRange2 = np.loadtxt("/home/philipp/compY/d0_E_Merge/d0_120/d12_120_Ranges")
data2 = np.loadtxt("Histograms/ExpEGamma_661/d0_120/d12_120")
dataRange2 = np.loadtxt("Histograms/ExpEGamma_661/d0_120/d12_120_Ranges")


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
colors2 = ["royalblue","orange","r"]

#plt.figure(4, figsize=(5, 3))
#plt.clf()

fig,ax = plt.subplots(2,figsize=(5,6),sharex=True)

markers =["o","^","x"]

msizes=[3.5,3.5,3.5]

for i in range(len(data)):
    #if i % 30 != 0 or np.sum(data[i,:]) == 0 or i == 0:
    #    continue
    if i*4 == 120 or i*4 == 360 or i*4 == 520:
        ax[0].plot(xbins,data[i,:],color=colors2[iter],ls='None',marker=markers[iter],ms=msizes[iter],label="$E_\\mathrm{dep} = "+str(i*4)+"$ keV")
        ax[0].vlines(dataRange[i,0],0,0.025,color=colors2[iter],linestyles='dashed',lw=1.5)
        ax[0].vlines(dataRange[i,1],0,0.025,color=colors2[iter],linestyles='dashed',lw=1.5)
        ax[1].plot(xbins,data2[i,:],color=colors2[iter],ls='None',marker=markers[iter],ms=msizes[iter],label="$E_\\mathrm{dep} = "+str(i*4)+"$ keV")
        ax[1].vlines(dataRange2[i,0],0,1,color=colors2[iter],linestyles='dashed',lw=1.5)
        ax[1].vlines(dataRange2[i,1],0,1,color=colors2[iter],linestyles='dashed',lw=1.5)
        iter += 1
        print(i*4,dataRange[i,0],dataRange[i,1])
ax[0].tick_params(axis='both', which='major', labelsize=15)
ax[0].tick_params(axis='both', which='minor', labelsize=10) 
ax[1].tick_params(axis='both', which='major', labelsize=15)
ax[1].tick_params(axis='both', which='minor', labelsize=10) 
ax[1].set_xlabel("$\\vartheta$ (deg)",fontsize=17)
ax[0].set_ylabel("$P(E_\\mathrm{dep},\\vartheta)$",fontsize = 17)
ax[1].set_ylabel("$P(E_\\mathrm{dep},\\vartheta)$",fontsize = 17)
ax[0].set_ylim(0,0.032)
ax[1].set_ylim(0,0.12)
ax[0].text(188,0.032/2,"$d_{0,1} = d_{1,2} = 12$ mm",rotation=270,size = 14,ha='center', va='center')
ax[1].text(188,0.06,"$d_{0,1} = d_{1,2} = 120$ mm",rotation=270,size = 14,ha='center', va='center')
ax[0].text(160,0.032*0.8,"(a)",size = 14,ha='center', va='center')
ax[1].text(160,0.12*0.8,"(b)",size = 14,ha='center', va='center')

for i in range(2):
    ax[i].set_xlim(-2,182)
ax[0].legend(loc=9,frameon=False,fontsize=11,ncol=2)
plt.subplots_adjust(hspace=0.05)
plt.savefig("/home/philipp/FirstPaper/EX_new2.pdf",bbox_inches="tight")
