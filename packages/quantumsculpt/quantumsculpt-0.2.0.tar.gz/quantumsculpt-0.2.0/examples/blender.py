import sys
import os
import numpy as np
from quantumsculpt import Wavecar,BlenderRender

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
contcar = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'CONTCAR')
wf = Wavecar(filename, lgamma=False)

br = BlenderRender()
br.render_kohn_sham_state(wf=wf, outpath=ROOT, mo_indices=np.arange(0,wf.get_nbands()),
                          camera='x', contcar=contcar, camera_scale=8, ispin=1,
                          prefix='CO')