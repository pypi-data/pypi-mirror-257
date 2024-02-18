import unittest
import numpy as np
import sys
import os

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

import quantumsculpt as qs

class TestDosPlotting(unittest.TestCase):

    def test_generate_sets(self):
        # check that function returns a sorted list
        res = qs.dos_generate_sets([1,2], ['2s','2p_x'])
        self.assertEqual(res, ['1-2p_x', '1-2s', '2-2p_x', '2-2s'])
        print(res)
        
        # check that duplicates are pruned
        res = qs.dos_generate_sets([1,2], ['2s','2p_x', '2p_x'])
        self.assertEqual(res, ['1-2p_x', '1-2s', '2-2p_x', '2-2s'])
        
        res = qs.dos_generate_sets([1,2,1,2], ['2s','2p_x', '2p_x'])
        self.assertEqual(res, ['1-2p_x', '1-2s', '2-2p_x', '2-2s'])

if __name__ == '__main__':
    unittest.main()
