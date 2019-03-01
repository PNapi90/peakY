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

data = np.loadtxt("Histograms/TmpEGamma_661/d0_"+str(d0)+"/d12_"+str(d12))

for i in range(len(data)):
    norm = np.sum(data[i,:])
    if norm > 0:
        data[i,:] /= norm

psi = np.linspace(0,180,1000)
comp = Ecomp(psi)

from matplotlib import cm

x = np.array([i for i in range(181)])
y = np.array([i*4 for i in range(175)])

X,Y = np.meshgrid(x,y)

Z  = data

from matplotlib.colors import LogNorm

#norm = cm.colors.Normalize(vmax=abs(Z).max(), vmin=-abs(Z).max())
cmap = cm.jet

from matplotlib import colors, ticker, cm

plt.figure(1,figsize=(5,3))
plt.clf()

#fig, _axs = plt.subplots(nrows=2, ncols=2)
#fig.subplots_adjust(hspace=0.3)
#axs = _axs.flatten()

#plt.contourf(X, Y, Z, 100,norm=LogNorm(),
#                     cmap=cm.jet)



#contours = plt.contour(X, Y, Z,10,colors="white",)
#plt.clabel(contours, inline=True, fontsize=8)
im = plt.imshow(data,cmap = plt.cm.jet,origin="lower",extent=[0,181,0,700],aspect="auto",interpolation="None",norm=LogNorm(vmin=1e-5, vmax=2e-2))
plt.plot(psi,comp,color="k",ls='--',lw=1.5)
cbar = plt.colorbar(im)
cbar.set_label("$ P ( E_{\\text{dep}},\\vartheta)$",rotation=270,fontsize=15)
cbar.ax.get_yaxis().labelpad = 15
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='minor', labelsize=10)
plt.xlabel("$\\vartheta$ (deg)",fontsize=17)
plt.ylabel("$E_{\\mathrm{dep}}$ (keV)",fontsize = 17)
plt.ylim([0,630])

plt.savefig("/home/philipp/FirstPaper/PEdepTh_Again2.pdf",bbox_inches="tight")


# It is not necessary, but for the colormap, we need only the
# number of levels minus 1.  To avoid discretization error, use
# either this number or a large number such as the default (256).

# If we want lines as well as filled regions, we need to call
# contour separately; don't try to change the edgecolor or edgewidth
# of the polygons in the collections returned by contourf.
# Use levels output from previous call to guarantee they are the same.

#cset2 = axs[0].contour(X, Y, Z, cset1.levels, colors='k')

"""
print(len(data),len(data[0]))
plt.figure(1,figsize=(5,3))
plt.clf()
plt.imshow(data,cmap = plt.cm.jet,origin="lower",extent=[0,181,0,700],aspect="auto",interpolation="None",norm=LogNorm())
plt.plot(psi,comp,color="k",ls='--',lw=1.5)
cbar = plt.colorbar()
cbar.set_label("$ P ( E_{\\text{dep}},\\vartheta)$",rotation=270,fontsize=15)
cbar.ax.get_yaxis().labelpad = 15
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='minor', labelsize=10)
plt.xlabel("$\\vartheta$ (deg)",fontsize=17)
plt.ylabel("$E_{\\mathrm{dep}}$ (keV)",fontsize = 17)
"""