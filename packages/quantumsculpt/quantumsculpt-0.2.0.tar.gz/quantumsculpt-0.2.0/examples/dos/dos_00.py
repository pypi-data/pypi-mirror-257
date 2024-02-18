import os
import matplotlib.pyplot as plt
from quantumsculpt import DensityOfStates
import quantumsculpt as qs

# load the DOSCAR.lobster file via a DensityOfStates class
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
dos = DensityOfStates(filename)

print(dos.get_nr_atoms())
energies = dos.get_energies()
print(energies.shape, energies[0], energies[-1])
totaldos = dos.get_total_dos()
print(totaldos.keys())

fig, ax = plt.subplots(1, 1, dpi=144, figsize=(4,4))
qs.plot_total_dos(ax, 
                  dos, 
                  grid=True, 
                  ylim=(-25,5),
                  title='Total DOS CO(g)')