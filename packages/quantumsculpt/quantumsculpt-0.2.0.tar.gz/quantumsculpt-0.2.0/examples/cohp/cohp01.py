import os
import matplotlib.pyplot as plt
from quantumsculpt import CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs

# load the COHPCAR.lobster file via a CrystalOrbitalHamiltonPopulation class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

# specify which collections of projections to plot
sigmasetcohp = qs.cohp_generate_sets('O2', 'C1', ['2s','2p_x'])
pisetcohp = qs.cohp_generate_sets('O2', 'C1', ['2p_y','2p_z'])
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

fig, ax = plt.subplots(1,1, dpi=144)

qs.plot_gathered_cohp(ax,
                      cohp,
                      collections=collection,
                      grid=True,
                      title=r'$\sigma / \pi$-COHP CO$_{\mathrm{ads}}$',
                      ylim=(-25,5),
                      legend=True)