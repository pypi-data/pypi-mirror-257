import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from pytessel import PyTessel

def main():

    # add a reference to load the module
    ROOT = os.path.dirname(__file__)
    sys.path.append(os.path.join(ROOT, '..'))
    
    from cloudwatcher import Wavecar,BlenderRender
    
    filename = os.path.join('D:/','Data','data_xianxuan','COHgas','Nelectron_12','ISPIN2','total_COH','WAVECAR')
    contcar= os.path.join('D:/','Data','data_xianxuan','COHgas','Nelectron_12','ISPIN2','total_COH','CONTCAR')
    #filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'WAVECAR_aligned')
    #contcar = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'CONTCAR_aligned')
    wf = Wavecar(filename, lgamma=False)
    
    # always first test a single image via a contourplot or similar
    # cgrid = wf.get_grid(order='xyz') * 4 # create a custom grid to enhance the resolution
    # unitcell = wf.get_unitcell()
    
    # psi = wf.build_wavefunction(ispin=1, ikpt=1, iband=4, norm=True,
    #                             ngrid=cgrid, order='zyx')
    
    # plt.figure(dpi=144)
    # plt.imshow(psi[:,psi.shape[1]//2,:].real, interpolation='bicubic',
    #            origin='lower', extent=(0,unitcell[0,0],0,unitcell[2,2]),
    #            vmin=-0.1, vmax=0.1, cmap='PRGn')
    # plt.colorbar()
    # plt.show()

    br = BlenderRender()
    br.render_kohn_sham_state(wf=wf, outpath=ROOT, mo_indices=np.arange(0,6),
                              camera='z', contcar=contcar, camera_scale=8, ispin=1,
                              prefix='COH_SPINUP')
    br.render_kohn_sham_state(wf=wf, outpath=ROOT, mo_indices=np.arange(0,6),
                              camera='z', contcar=contcar, camera_scale=8, ispin=2,
                              prefix='COH_SPINDOWN')
    
def build_isosurface(filename, scalarfield, grid, unitcell, isovalue):
    # generate some data
    pytessel = PyTessel()
    vertices, normals, indices = pytessel.marching_cubes(scalarfield.flatten(), grid, unitcell.flatten(), isovalue)
    pytessel.write_ply(filename, vertices, normals, indices)
    
if __name__ == '__main__':
    main()
