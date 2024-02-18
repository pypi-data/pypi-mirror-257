import os
import matplotlib.pyplot as plt
import numpy as np
from quantumsculpt import DensityOfStates, CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs

ROOT = os.path.dirname(__file__)

###############################################################################
# DOS AND COHP FOR CO IN THE GAS PHASE
###############################################################################

#
# COLLECT DATA
#

# load DOS and COHP files
filename_dos = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
dos = DensityOfStates(filename_dos)
filename_cohp = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename_cohp)

# try to find perfect peak barriers
energies = dos.get_energies()
totaldos = dos.get_total_dos()['states']

# try to find the peaks via fitting
peaks = qs.find_peaks(energies, totaldos)
fitres = qs.fit_gaussians(energies, totaldos, peaks[1])

# construct bins based on fitting
bins = []
nsigma = 6
for g in fitres['gaussians']:
    bins.append([g['mu'] - nsigma*g['sigma'], g['mu'] + nsigma*g['sigma']])

#
# PLOT RESULTS
#

# create figure
fig, ax = plt.subplots(2,4, dpi=144, figsize=(14,8))

# plot (0,0): total DOS for CO
qs.plot_total_dos(ax[0,0], 
                  dos, 
                  grid=True,
                  bins=bins,
                  ylim=(-25,5),
                  title=r'Total DOS CO$_{\mathrm{g}}$')

# specify which collections of projections to plot
collection = [
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$\sigma$', 'color': qs.colors.red, 'style': 'filled'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$\pi$', 'color': qs.colors.blue, 'style': 'filled'},
    {'set': ['all-2s', 'all-2p_x'], 'legendlabel' : '$int - \sigma$', 'color': qs.colors.red, 'style': 'integrated'},
    {'set': ['all-2p_y', 'all-2p_z'], 'legendlabel' : '$int - \pi$', 'color': qs.colors.blue, 'style': 'integrated'}
]

# plot (0,1): DOS for collections of atomic orbitals
qs.plot_gathered_dos(ax[0,1], 
                     dos,
                     collection, 
                     grid=True, 
                     ylim=(-25,5), 
                     legend=True,
                     title=r'$\sigma / \pi$-DOS CO$_{\mathrm{(g)}}$',
                     bins=bins,
                     legendloc='lower right')

# plot (0,2): Averaged COHP between C and O
qs.plot_averaged_cohp(ax[0,2],
                      cohp, 
                      grid=True,
                      bins=bins,
                      ylim=(-25,5),
                      icohp=True,
                      title=r'Averaged COHP CO$_{\mathrm{(g)}}$',
                      legend=True,
                      legendloc='upper left')

# build collections for COHP plot showing specific interactions
sigmaset = qs.cohp_generate_sets('C1', 'O2', ['2s','2p_x'])
piset = qs.cohp_generate_sets('C1', 'O2', ['2p_y','2p_z'])

# specify which collections of projections to plot
collection = [
    {'set': sigmaset, 
     'legendlabel' : '$\sigma$', 
     'color': qs.colors.red, 
     'style': 'filled'},
    {'set': piset, 
     'legendlabel' : '$\pi$', 
     'color': qs.colors.blue, 
     'style': 'filled'},
    {'set': sigmaset, 
     'legendlabel' : '$int - \sigma$', 
     'color': qs.colors.red, 
     'style': 'integrated'},
    {'set': piset, 
     'legendlabel' : '$int - \pi$', 
     'color': qs.colors.blue, 
     'style': 'integrated'}
]

# plot (0,3): COHP for specific interactions
qs.plot_gathered_cohp(ax[0,3],
                      cohp,
                      collections=collection,
                      grid=True,
                      bins=bins,
                      title=r'$\sigma / \pi$-COHP CO$_{\mathrm{(g)}}$',
                      ylim=(-25,5),
                      legend=True,
                      legendloc='lower right')

#
# PERFORM INTEGRATION
#

# add one more bin to integrate up to Fermi
# note that to get the total number of electrons correct for
# gas phase species, we need set the upper bound a bit above
# the Fermi-level
bins.append([-35,0.5])

# dos integration
colllection = qs.cast_to_collection(['all-2s', 'all-2p_x'], ['all-2p_y', 'all-2p_z'])
cogasdos = qs.integrate_dos_bins(dos, bins, collection)

# cohp integration

collection = qs.cast_to_collection(sigmaset, piset)
cohpgasdos = qs.integrate_cohp_bins(cohp, bins, collection)

###############################################################################
# DOS AND COHP FOR CO ADSORBED ON A Co(0001) lattice
###############################################################################

# load DOS and COHP files
filename_dos = os.path.join(ROOT, '..', '..', 'samples', 'CO_Co0001_hcp', 'DOSCAR.lobster')
dos = DensityOfStates(filename_dos)
filename_cohp = os.path.join(ROOT, '..', '..', 'samples', 'CO_Co0001_hcp', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename_cohp)

# specify where to place the bins for orbital deconvolution
bins = [
    (-23.0,-21.5),
    (-10.5,-9.4),
    (-9,-5),
    (-5,0),
    (-35,0.0),
]

#
# PLOT RESULTS
#

# specify which collection of interaction to plot
collection = [
    {'set': ['65-all','66-all'],
     'legendlabel' : 'total', 
     'color': qs.colors.grey, 
     'style': 'filled',
     'stack': True},
    {'set': ['65-all','66-all'], 
     'legendlabel' : 'int total', 
     'color': qs.colors.black, 
     'style': 'integrated'},
]

# plot (1,0): Total DOS on C and O
qs.plot_gathered_dos(ax[1,0], 
                     dos, 
                     collection,
                     grid=True,
                     ylim=(-25,5),
                     legend=True,
                     addspins=True,
                     bins=bins,
                     title=r'Total DOS CO$_{\mathrm{ads}}$',
                     legendloc='lower right')

# specify which atomic orbitals to plot
sigmasetdos = qs.dos_generate_sets([65,66], ['2s','2p_x'])
pisetdos = qs.dos_generate_sets([65,66], ['2p_y','2p_z'])
collection = [
    {'set': sigmasetdos, 
     'legendlabel' : '$\sigma$', 
     'color': qs.colors.red, 
     'style': 'filled', 
     'stack': True},
    {'set': pisetdos, 
     'legendlabel' : '$\pi$', 
     'color': qs.colors.blue, 
     'style': 'filled', 
     'stack': True},
    {'set': sigmasetdos, 
     'legendlabel' : '$int - \sigma$', 
     'color': qs.colors.red, 
     'style': 'integrated'},
    {'set': pisetdos, 
     'legendlabel' : '$int - \pi$', 
     'color': qs.colors.blue, 
     'style': 'integrated'}
]

# plot (1,1): plot DOS for specific atomic orbital interactions
qs.plot_gathered_dos(ax[1,1], 
                     dos, 
                     collection,
                     grid=True,
                     ylim=(-25,5),
                     legend=True,
                     addspins=True,
                     bins=bins,
                     title=r'$\sigma / \pi$-DOS CO$_{\mathrm{ads}}$',
                     legendloc='lower right')

# plot (1,2): plot averaged COHP
qs.plot_averaged_cohp(ax[1,2], 
                      cohp, 
                      grid=True,
                      bins=bins,
                      ylim=(-25,5),
                      icohp=True,
                      title=r'Averaged COHP CO$_{\mathrm{ads}}$',
                      legend=True,
                      legendloc='upper left')

# specify which collections of projections to plot
sigmasetcohp = qs.cohp_generate_sets('O66', 'C65', ['2s','2p_x'])
pisetcohp = qs.cohp_generate_sets('O66', 'C65', ['2p_y','2p_z'])
collection = [
    {'set': sigmasetcohp, 
     'legendlabel' : '$\sigma$', 
     'color': qs.colors.red, 
     'style': 'filled',
     'stack': True},
    {'set': pisetcohp, 
     'legendlabel' : '$\pi$', 
     'color': qs.colors.blue, 
     'style': 'filled',
     'stack': True},
    {'set': sigmasetcohp, 
     'legendlabel' : '$int - \sigma$', 
     'color': qs.colors.red, 
     'style': 'integrated'},
    {'set': pisetcohp, 
     'legendlabel' : '$int - \pi$', 
     'color': qs.colors.blue, 
     'style': 'integrated'}
]

# plot (1,3): COHP for specific interactions
qs.plot_gathered_cohp(ax[1,3],
                      cohp,
                      collections=collection,
                      grid=True,
                      bins=bins,
                      title=r'$\sigma / \pi$-COHP CO$_{\mathrm{ads}}$',
                      ylim=(-25,5),
                      legend=True)

# dos integration
collection = qs.cast_to_collection(sigmasetdos, pisetdos)
coadsdos = qs.integrate_dos_bins(dos, bins, collection)

# cohp integration
collection = qs.cast_to_collection(sigmasetcohp, pisetcohp)
cohpadsdos = qs.integrate_cohp_bins(cohp, bins, collection)

# final adjustment plots
ax[0,0].set_xlim(0,12)
ax[0,1].set_xlim(0,12)
ax[1,0].set_xlim(0,12)
ax[1,1].set_xlim(0,12)
ax[0,2].set_xlim(-5,1)
ax[1,2].set_xlim(-5,1)
ax[0,3].set_xlim(-40,40)
ax[1,3].set_xlim(-40,40)

plt.tight_layout()

###############################################################################
# PLOT INTEGRATION RESULTS
###############################################################################

fig, ax = plt.subplots(1, 2, dpi=144)

from matplotlib.font_manager import FontProperties
font = FontProperties()
font.set_family('monospace')

# collect DOS data and visualize it
dosco_sigma_gas = [
    cogasdos[0]['idos'][0]['idos'],
    cogasdos[1]['idos'][0]['idos'],
    cogasdos[2]['idos'][0]['idos'] + cogasdos[3]['idos'][0]['idos'],
    0.0
]
dosco_pi_gas = [
    cogasdos[0]['idos'][1]['idos'],
    cogasdos[1]['idos'][1]['idos'],
    cogasdos[2]['idos'][1]['idos'] + cogasdos[3]['idos'][1]['idos'],
    0.0
]
dosco_sigma_ads = [
    coadsdos[i]['idos'][0]['idos'] for i in range(0,4)
]
dosco_pi_ads = [
    coadsdos[i]['idos'][1]['idos'] for i in range(0,4)
]

#
# PRODUCE BARGRAPH FOR DOS
#
colors = [
    qs.colors.red,
    qs.colors.blue,
    qs.colors.red,
    qs.colors.blue,
]

# left offset for labels
loffset = 12

# plot specific MOs
for i,(val,col) in enumerate(zip([dosco_sigma_gas, dosco_pi_gas, dosco_sigma_ads, dosco_pi_ads], colors)):    
    ax[0].barh(np.arange(0,4)+0.125+i*0.25, val, height=0.25, color=col,
               hatch='//' if i>=2 else None, edgecolor='black')
    for j,v in enumerate(val):
        ax[0].text(loffset, j + i * 0.25 + 0.05, '%+6.2f' % v, fontproperties=font,
                   color=col)

# plot totals
totaldosgas = cogasdos[-1]['idos'][0]['idos'] + cogasdos[-1]['idos'][1]['idos']
ax[0].barh(4.125, totaldosgas,
           height=0.25, color='#00000055', edgecolor='black')
ax[0].text(loffset, 4.05, '%+6.2f' % totaldosgas, fontproperties=font, color='grey')
totaldosads = coadsdos[-1]['idos'][0]['idos'] + coadsdos[-1]['idos'][0]['idos']
ax[0].barh(4.375, totaldosads,
           height=0.25, color='#000000', edgecolor='black')
ax[0].text(loffset, 4.255, '%+6.2f' % totaldosads, fontproperties=font, color='black')

ax[0].set_ylim(0,4.5)
ax[0].hlines([0,1,2,3,4], 0, 12, linestyle='--', color='black')
ax[0].set_yticks([0.5,1.5,2.5,3.5,4.25], ['$3\sigma$','$4\sigma$','$5\sigma+1\pi$','$2\pi$', 'total'])
ax[0].set_xlim(0,12)
ax[0].set_title('DOS')
ax[0].grid(linestyle='--', color='black', alpha=0.5)
ax[0].set_xlabel('iDOS [-]')

# collect COHP data and visualize it
cohp_sigma_gas = [
    cohpgasdos[0]['icohp'][0]['icohp'],
    cohpgasdos[1]['icohp'][0]['icohp'],
    cohpgasdos[2]['icohp'][0]['icohp'] + cohpgasdos[3]['icohp'][0]['icohp'],
    0.0,
]
cohp_pi_gas = [
    cohpgasdos[0]['icohp'][1]['icohp'],
    cohpgasdos[1]['icohp'][1]['icohp'],
    cohpgasdos[2]['icohp'][1]['icohp'] + cohpgasdos[3]['icohp'][1]['icohp'],
    0.0,
]
cohp_sigma_ads = [
    cohpadsdos[i]['icohp'][0]['icohp'] for i in range(0,4)
]
cohp_pi_ads = [
    cohpadsdos[i]['icohp'][1]['icohp'] for i in range(0,4)
]

#
# PRODUCE BARGRAPH FOR COHP
#

# left offset for labels
loffset = 6

# plot specific MOs
for i,(val,col) in enumerate(zip([cohp_sigma_gas, cohp_pi_gas, cohp_sigma_ads, cohp_pi_ads], colors)):
    ax[1].barh(np.arange(0,4)+0.125+i*0.25, val, height=0.25, color=col,
               hatch='//' if i>=2 else None, edgecolor='black')
    for j,v in enumerate(val):
        ax[1].text(loffset, j + i * 0.25 + 0.05, '%+6.2f' % v, fontproperties=font,
                   color=col)

# plot totals
totalcohpgas = cohpgasdos[-1]['icohp'][0]['icohp'] + cohpgasdos[-1]['icohp'][1]['icohp']
ax[1].barh(4.125, totalcohpgas,
           height=0.25, color='#00000055', edgecolor='black')
ax[1].text(loffset, 4.05, '%+6.2f' % totalcohpgas, fontproperties=font, color='grey')
totalcohpads = cohpadsdos[-1]['icohp'][0]['icohp'] + cohpadsdos[-1]['icohp'][1]['icohp']
ax[1].barh(4.375, totalcohpads,
           height=0.25, color='#000000', edgecolor='black')
ax[1].text(loffset, 4.255, '%+6.2f' % totalcohpads, fontproperties=font, color='black')

ax[1].set_ylim(0,4.5)
ax[1].hlines([0,1,2,3,4], -25, 5, linestyle='--', color='black')
ax[1].set_yticks([0.5,1.5,2.5,3.5,4.25], ['$3\sigma$','$4\sigma$','$5\sigma+1\pi$','$2\pi$', 'total'])
ax[1].set_xlim(-25,5)
ax[1].set_title('COHP')
ax[1].grid(linestyle='--', color='black', alpha=0.5)
ax[1].set_xlabel('iCOHP [-]')

plt.tight_layout()