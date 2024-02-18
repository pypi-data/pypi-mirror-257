import os
import tempfile
import numpy as np
import json
import subprocess
import shutil
from sys import platform
from . import Wavecar

# try to import PyTessel but do not throw an error if it cannot be loaded
try:
    from pytessel import PyTessel
except ModuleNotFoundError:
    print('Cannot find module PyTessel')

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print('Cannot find module tqdm')

class BlenderRender:
    """
    This class leverages blender for rendering molecular orbitals
    """
    def __init__(self):
        self.executable = self.__find_blender()
        self.log = []
        print('******************************************************')
        print('WARNING: Blender rendering is an EXPERIMENTAL FEATURE.')
        print('******************************************************')
        if self.executable is None:
            raise Exception('Cannot find Blender executable')
        else:
            print('Found executable: %s' % self.executable)

    def render_kohn_sham_state(self, wf:Wavecar, outpath:str,
                               mo_indices=None, isovalue=0.03,
                               prefix='MO', negcol='E72F65', poscol='3F9EE7',
                               store_ply=False, camera='x', camera_scale=10,
                               resolution=512, contcar=None, ispin=1):

        if mo_indices is None:
            raise Exception('You need to specify which orbitals to render')

        camera_location, camera_rotation = self.__build_camera(camera)

        # build a temporary folder
        tempdir = tempfile.mkdtemp()

        # create xyz file
        if contcar is not None:
            xyzfile = os.path.join(tempdir, 'mol.xyz')
            self.__build_xyz_from_contcar(contcar, xyzfile)
        else:
            xyzfile = None

        # produce somewhat higher-resolution grid
        grid = wf.get_grid() * 4

        pbar = tqdm(mo_indices)
        for idx in pbar:
            # build isosurfaces
            pbar.set_description('Producing isosurfaces (#%i)' % (idx+1))
            plyfile = os.path.join(tempdir, '%s_%04i' % (prefix,idx+1))
            plypos, plyneg = self.__build_isosurface(plyfile, wf, idx+1, grid, 
                                                     isovalue, ispin=ispin)
            
            # copy .ply upon request back to output folder
            if store_ply:
                shutil.copy(plypos, os.path.join(outpath, 'MO%03i_pos.ply' % idx))
                shutil.copy(plyneg, os.path.join(outpath, 'MO%03i_neg.ply' % idx))

            # execute blender
            pbar.set_description('Producing molecular orbital (#%i)' % (idx+1))
            outfile = os.path.join(outpath, '%s_%04i.png' % (prefix,idx+1))
            logoutput = self.__run_blender(plypos, plyneg, outfile, tempdir, negcol, poscol,
                                           resolution=resolution, camera_scale=camera_scale,
                                           camera_location=camera_location,
                                           camera_rotation=camera_rotation,
                                           xyzfile=xyzfile)

            self.log.append("### START LOG: MOLECULAR ORBITAL %i ###" % (idx+1))
            for line in logoutput.splitlines():
                self.log.append(line.decode('utf-8'))
            self.log.append("### END LOG: MOLECULAR ORBITAL %i ###" % (idx+1))

        shutil.rmtree(tempdir)

        # store log in same path
        with open(os.path.join(outpath, 'renderlog.txt'), 'w') as f:
            for line in self.log:
                f.write(line + '\n')
            f.close()

    def get_executable(self):
        """
        Get the Blender executable
        """
        return self.executable

    def __find_blender(self):
        """
        Find the Blender executable
        """
        if platform == "linux" or platform == "linux2":
            ex = '/opt/blender-3.3.11-linux-x64/blender' # preferred version and path
            if os.path.exists(ex):
                return ex

            print('Cannot find proper Blender executable. For Linux, please install Blender LTS 3.3.11 in /opt/blender-3.3.11-linux-x64/.')
            print('Blender can be obtained via: https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.3/blender-3.3.11-linux-x64.tar.xz')
            print('For more details on how to install Blender, please consult the instructions in the manual: https://pyqint.imc-tue.nl/')

            return None
        elif platform == 'win32':
            searchpath = os.path.join('C:\\','Program Files','Blender Foundation')
            name = 'blender.exe'
            results = []
            for root, dirs, files in os.walk(searchpath):
                if name in files:
                    results.append(os.path.join(root, name))

            for res in results:
                if '3.3' in res:
                    return res
        else:
            raise Exception('Your platform is not supported for Blender')

        return None

    def __run_blender(self, negfile, posfile, pngfile, cwd, negcol, poscol,
                      camera_location=(-10,0,0), camera_rotation=(np.pi/2,0,-np.pi/2), 
                      camera_scale=10, resolution=512, xyzfile=None):
        # set path to xyz file
        blendpysrc = os.path.join(os.path.dirname(__file__), 'blender', 'blender_render_molecule.py')
        blendpydst = os.path.join(cwd, 'blender_render_molecule.py')
        shutil.copyfile(blendpysrc, blendpydst)

        manifest = {
            'mo_colors' : {
                'neg': negcol,
                'pos': poscol,
            },
            'mo_name' : 'isosurface',
            'mo_neg_path' : negfile,
            'mo_pos_path' : posfile,
            'png_output': pngfile,
            'bond_thickness': 0.2,
            'atom_radii' : {
                'H': 0.3,
                'N': 0.5,
                'C': 0.5,
                'O': 0.5,
            },
            'atom_colors' : {
                'H': 'FFFFFF',
                'N': '0000FF',
                'C': '000000',
                'O': 'DD0000',
            },
            'resolution': resolution,
            'camera_location': camera_location,
            'camera_rotation': camera_rotation,
            'camera_scale' : camera_scale
        }
        
        if xyzfile is not None:
            manifest['xyzfile'] = xyzfile

        with open(os.path.join(cwd, 'manifest.json'), 'w') as f:
            f.write(json.dumps(manifest))

        # run blender
        out = subprocess.check_output(
            [self.executable, '-b', '-P', blendpydst],
            cwd=cwd
        )

        return out

    def __build_isosurface(self, filename, wavefunction, iband, grid, isovalue,
                           ispin=1):
        """
        Construct isosurfaces from PyQInt output
        """
        # generate some data
        isovalue = np.abs(isovalue)

        psi = wavefunction.build_wavefunction(ispin=ispin, 
                                              ikpt=1, 
                                              iband=iband, 
                                              norm=True,
                                              ngrid=grid,
                                              order='zyx')
        psi = wavefunction.optimize_real(psi).real
        unitcell = wavefunction.get_unitcell()

        pytessel = PyTessel()
        vertices, normals, indices = pytessel.marching_cubes(psi.flatten(), grid, unitcell.flatten(), isovalue)
        posfile = filename + '_pos.ply'
        pytessel.write_ply(posfile, vertices, normals, indices)

        vertices, normals, indices = pytessel.marching_cubes(psi.flatten(), grid, unitcell.flatten(), -isovalue)
        negfile = filename + '_neg.ply'
        pytessel.write_ply(negfile, vertices, normals, indices)

        return posfile, negfile
    
    def __build_camera(self, camsetting='x'):
        
        if camsetting == 'x':
            camera_location = (-10,0,0)
            camera_rotation = (np.pi/2,0,-np.pi/2)
        elif camsetting == 'z':
            camera_location = (0,0,10)
            camera_rotation = (0,0,0)
        elif camsetting == 'xyz':
            camera_location = (7.5,5,9)
            camera_rotation = (np.radians(45),0,np.radians(125))
            
        return camera_location, camera_rotation
    
    def __build_xyz_from_contcar(self, infile, outfile):
        molecule = []
        
        f = open(infile, 'r')
        f.readline() # skip header
        
        # build unitcell
        scalar = float(f.readline())
        unitcell = np.zeros((3,3))
        for i in range(0,3):
            unitcell[i,:] = np.array([float(v) for v in f.readline().split()])
        unitcell *= scalar
        
        # grab atoms
        atoms = f.readline().split()
        nratoms = [int(v) for v in f.readline().split()]
        line = f.readline()
        if 'Selective dynamics' in line:
            f.readline() # assume Direct
        for a,n in zip(atoms, nratoms):
            for i in range(n):
                d = np.array([float(v) for v in f.readline().split()[0:3]])
                molecule.append([a, (d - np.ones(3) * 0.5) @ unitcell])
        f.close()
        
        # write xyzfile
        f = open(outfile, 'w')
        f.write('%i' % np.sum(nratoms) + '\n')
        f.write('\n')

        for a in molecule:
            elname = a[0]
            f.write('%s  %12.6f  %12.6f  %12.6f\n' % (elname, a[1][0],
                                                              a[1][1],
                                                              a[1][2]))

        f.close()