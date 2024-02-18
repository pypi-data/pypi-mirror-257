import sys
import os
import numpy as np
from quantumsculpt import Wavecar,BlenderRender

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

# path to WAVECAR and CONTCAR files
filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
contcar = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'CONTCAR')

# set output folder and create it if it does not yet exists
output = os.path.join(ROOT, '..', '..', 'output')
if not os.path.exists(output):
    os.mkdir(output)

# load WAVECAR
wf = Wavecar(filename, lgamma=False)

# construct BlenderRender object
br = BlenderRender()

# render all MOs
br.render_kohn_sham_state(wf=wf, outpath=output, mo_indices=np.arange(0,wf.get_nbands()),
                          camera='x', contcar=contcar, camera_scale=10, ispin=1,
                          prefix='CO')