import os
import matplotlib.pyplot as plt
from quantumsculpt import Wavecar
import numpy as np

# add a reference to load the module
ROOT = os.path.dirname(__file__)
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
wf = Wavecar(filename, lgamma=False)

unitcell = wf.get_unitcell()
grid = wf.get_grid() * 4
ao = wf.build_wavefunction(1, 1, 2, order='zyx', ngrid=grid)
dV = wf.get_volume() / np.prod(grid)
edens = np.einsum('ijk,ijk', ao, ao.conjugate()).real * dV
print('Total electron density: ', edens)

from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots(1,2, dpi=144)

xx = np.linspace(0, unitcell[0,0], grid[0])
zz = np.linspace(0, unitcell[2,2], grid[2])

levels = np.linspace(-2.0,2.0,17)
im = ax[0].contourf(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
           extent=(0, unitcell[0,0], 0, unitcell[2,2]),
           vmin=levels[0], vmax=levels[-1],
           cmap='PiYG', levels=levels)
ax[0].contour(xx, zz, ao[:,grid[1]//2,:].real, origin='lower',
           extent=(0, unitcell[0,0], 0, unitcell[2,2]),
           vmin=levels[0], vmax=levels[-1],
           colors='black', levels=levels,
           linewidths=0.5)

# create colorbar
divider = make_axes_locatable(ax[0])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(im, cax=cax, orientation='vertical')

im = ax[1].contourf(xx, zz, ao[:,grid[1]//2,:].imag, origin='lower',
           extent=(0, unitcell[0,0], 0, unitcell[2,2]),
           vmin=levels[0], vmax=levels[-1],
           cmap='PiYG', levels=levels)
ax[1].contour(xx, zz, ao[:,grid[1]//2,:].imag, origin='lower',
           extent=(0, unitcell[0,0], 0, unitcell[2,2]),
           vmin=levels[0], vmax=levels[-1],
           colors='black', levels=levels,
           linewidths=0.5)

# create colorbar
divider = make_axes_locatable(ax[1])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(im, cax=cax, orientation='vertical')

ax[0].set_title('Real part')
ax[1].set_title('Imaginary part')

for i in range(0,2):
    ax[i].set_aspect('equal', adjustable='box')
    ax[i].set_xlabel('x-coordinate [Å]')
    ax[i].set_ylabel('z-coordinate [Å]')
plt.tight_layout()