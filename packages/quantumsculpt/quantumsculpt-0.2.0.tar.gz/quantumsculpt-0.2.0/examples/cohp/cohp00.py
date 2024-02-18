import os
import matplotlib.pyplot as plt
from quantumsculpt import CrystalOrbitalHamiltonPopulation
import quantumsculpt as qs

# load the COHPCAR.lobster file via a CrystalOrbitalHamiltonPopulation class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
cohp = CrystalOrbitalHamiltonPopulation(filename)

print(len(cohp.get_dataitems()))
energies = cohp.get_energies()
print(energies.shape, energies[0], energies[-1])
avgcohp = cohp.get_dataitem(0)
print(avgcohp.keys())
print(avgcohp['type'])

print(cohp)

fig, ax = plt.subplots(1,1, dpi=144)
qs.plot_averaged_cohp(ax, 
                      cohp, 
                      icohp=True, 
                      grid=True,
                      ylim=(-30,5))