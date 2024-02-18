import unittest
import numpy as np
import sys
import os
from os import walk

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

from quantumsculpt import DensityOfStates
import quantumsculpt as qs

class TestDOS(unittest.TestCase):

    def test_read_doscar(self):
        filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
        dos = DensityOfStates(filename)
        
        self.assertEqual(dos.get_nr_atoms(), 2)
        self.assertEqual(dos.get_npts(), 801)
    
        # check integrity of total DOS
        total_dos = dos.get_total_dos()
        keys = ('energies', 'states','istates')
        for key in keys:
            self.assertTrue(key in total_dos, msg='No %s found' % key)
        self.assertEqual(len(total_dos['energies']), 801)

        dos_atom = dos.get_dos_atom(1)
        keys = ('states', 'atomid', 'atomnumber', 'labels')
        for key in keys:
            self.assertTrue(key in dos_atom)
        self.assertEqual(dos_atom['atomnumber'], 6)
        self.assertEqual(dos_atom['atomid'], 1)
        self.assertEqual(len(dos_atom['labels']), 4)
        
        dos_atom = dos.get_dos_atom(2)
        keys = ('states', 'atomid', 'atomnumber', 'labels')
        for key in keys:
            self.assertTrue(key in dos_atom)
        self.assertEqual(dos_atom['atomnumber'], 8)
        self.assertEqual(dos_atom['atomid'], 2)
        self.assertEqual(len(dos_atom['labels']), 4)
        
        keys = ('states', 'label')
        for key in keys:
            self.assertTrue(key in dos_atom['states'][0], msg='No %s found' % key)
            
    def test_dos_integration(self):
        for d in ['pbe', 'hse06', 'b3lyp']:
            filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', d, 'DOSCAR.lobster')
            dos = DensityOfStates(filename)
            
            # set atomic orbitals
            collections = [{'set': 'all-all'}]
            
            # set integration bins
            bins = [(-50,0.5)]
    
            nstates = qs.integrate_dos_bins(dos, bins, collections)[0]['idos'][0]['idos']
            np.testing.assert_almost_equal(nstates, 10.0, decimal=3)
        
        filename = os.path.join(ROOT, '..', 'samples', 'hco_gasphase', 'DOSCAR.lobster')
        dos = DensityOfStates(filename)
        
        # set atomic orbitals
        collections = [{'set': 'all-all'}]
        
        # set integration bins
        bins = [(-50.0, 0.05)]

        nstates = qs.integrate_dos_bins(dos, bins, collections)[0]['idos'][0]['idos']
        np.testing.assert_almost_equal(nstates, 12.11, decimal=2)
        
        filename = os.path.join(ROOT, '..', 'samples', 'hco_gasphase', 'DOSCAR2.lobster')
        dos = DensityOfStates(filename)
        
        # set atomic orbitals
        collections = [{'set': 'all-all'}]
        
        # set integration bins
        bins = [(-50.0, 0.00)]

        nstates = qs.integrate_dos_bins(dos, bins, collections)[0]['idos'][0]['idos']
        np.testing.assert_almost_equal(nstates, 12.0, decimal=3)
        

if __name__ == '__main__':
    unittest.main()
