import unittest
import numpy as np
import sys
import os

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, '..'))

from quantumsculpt import Wavecar

class TestWavecar(unittest.TestCase):

    def test_wavecar_co_pbe(self):
        """
        Test reading WAVECAR file and extracting data
        """
        filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
        wc = Wavecar(filename, lgamma=False)
        self.assertEqual(wc.get_nspin(), 1)
        self.assertEqual(wc.get_recl(), 144304)
        self.assertEqual(wc.get_rtag(), 45200)
        self.assertEqual(wc.get_precision(), 'Single precision, 64 bit complex values')        
        np.testing.assert_almost_equal(wc.get_encut(), 400.0)
        np.testing.assert_almost_equal(wc.get_unitcell(), np.diag([10,10,10]))
        self.assertEqual(wc.get_nbands(), 10)
        self.assertEqual(wc.get_nkpoints(), 1)
        self.assertEqual(wc.get_nrplanewaves()[0], 18037)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,1), -32.186826, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,2), -15.689711, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,3), -12.956668, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,4), -12.956667, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,5), -10.192438, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,6),  -1.048337, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,7),  -1.048336, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,8),  -0.141665, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,9),   1.172259, decimal=5)
        np.testing.assert_almost_equal(wc.get_eigenvalue(1,1,10),  1.291492, decimal=5)
        
    def test_wavefunction_mixing(self):
        """
        Test mixing between real and imaginary parts for the wave function
        """
        filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
        wc = Wavecar(filename, lgamma=False)
        psi = wc.build_wavefunction(ispin=1, ikpt=1, iband=2)
        psi_opt = wc.optimize_real(psi)
        dV = wc.get_volume() / np.prod(wc.get_grid())
        sumreal = np.sum(psi_opt.real**2) * dV
        sumimag = np.sum(psi_opt.imag**2) * dV
        np.testing.assert_almost_equal(sumreal, 1.0, decimal=5)
        np.testing.assert_almost_equal(sumimag, 0.0, decimal=5)
        
    def test_wavecar_co(self):
        """
        Test WAVECAR where the CO molecule is aligned with the z-axis
        and where a GAMMA-POINT calculation is used
        """
        filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'WAVECAR')
        wc = Wavecar(filename, lgamma=False)
        self.assertEqual(wc.get_nspin(), 1)
        self.assertEqual(wc.get_recl(), 144304)
        self.assertEqual(wc.get_rtag(), 45200)
        self.assertEqual(wc.get_precision(), 'Single precision, 64 bit complex values')
        np.testing.assert_almost_equal(wc.get_encut(), 400.0)
        np.testing.assert_almost_equal(wc.get_unitcell(), np.identity(3)*10)
        self.assertEqual(wc.get_nbands(), 10)
        self.assertEqual(wc.get_nkpoints(), 1)
        np.testing.assert_almost_equal(wc.get_occupancies()[0,0], [1., 1., 1., 1., 1., 0., 0., 0., 0., 0.])
        self.assertEqual(wc.get_nrplanewaves()[0], 18037)
        
        # check normalization for single wave function
        psi = wc.read_pseudo_wavefunction(1, 1, 1, norm=True, rescale=True)
        total = np.sum(psi * psi.conjugate()).real
        self.assertAlmostEqual(total, 1.0, places=4)
        
        # check that all wave functions are normalized
        cellvolume = wc.get_volume() / np.prod(wc.get_grid())
        for i in range(0,9):
            psi = wc.build_wavefunction(ispin=1, ikpt=1, iband=i+1)
            total = np.sum(psi * psi.conjugate()).real * cellvolume
            self.assertAlmostEqual(total, 1.0, places=4)
            
        # test constructing on a custom grid
        cgrid = wc.get_grid() * 8
        cellvolume = wc.get_volume() / np.prod(cgrid)
        np.testing.assert_almost_equal(cgrid, np.ones(3) * 280)
        psi = wc.build_wavefunction(ispin=1, ikpt=1, iband=i+1, ngrid=cgrid)
        total = np.sum(psi * psi.conjugate()).real * cellvolume
        self.assertAlmostEqual(total, 1.0, delta=1e-2/2) # allow error of half percent
        
        
        
if __name__ == '__main__':
    unittest.main()
