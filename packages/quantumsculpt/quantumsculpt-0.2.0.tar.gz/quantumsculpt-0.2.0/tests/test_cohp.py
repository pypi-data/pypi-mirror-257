import unittest
import numpy as np
import sys
import os

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

from quantumsculpt import CrystalOrbitalHamiltonPopulation as COHP

class TestDOS(unittest.TestCase):

    def test_read_doscar(self):
        filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
        cohp = COHP(filename)
        
        self.assertEqual(len(cohp.get_dataitems()), 18)
        self.assertEqual(cohp.get_spin_state(), 'restricted')

if __name__ == '__main__':
    unittest.main()
