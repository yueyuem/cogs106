#!/usr/bin/python3.8

import unittest
from SignalDetection import SignalDetection

class TestSignalDetection(unittest.TestCase):

    def test_d_prime_zero(self):
        sd   = SignalDetection(15, 5, 15, 5)
        expected = 0
        obtained = sd.d_prime()
        # Compare calculated and expected d-prime
        self.assertAlmostEqual(obtained, expected, places=10)

    def test_d_prime_nonzero(self):
        sd   = SignalDetection(15, 10, 15, 5)
        expected = -0.421142647060282
        obtained = sd.d_prime()
        # Compare calculated and expected d-prime
        self.assertAlmostEqual(obtained, expected, places=10)

    def test_criterion_zero(self):
        sd   = SignalDetection(5, 5, 5, 5)
        # Calculate expected criterion
        expected = 0
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertAlmostEqual(obtained, expected, places=10)

    def test_criterion_nonzero(self):
        sd   = SignalDetection(15, 10, 15, 5)
        # Calculate expected criterion
        expected = -0.463918426665941
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertAlmostEqual(obtained, expected, places=10)

    def test_addition(self):
        sd = SignalDetection(1, 1, 2, 1) + SignalDetection(2, 1, 1, 3)
        expected = SignalDetection(3, 2, 3, 4).criterion()
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertEqual(obtained, expected)
    
    def test_addition_fail(self):
        #this test is testing if the addition of non-SignalDetection class is going
        #to corrupt and raise exception
        sd = SignalDetection(1, 1, 2, 1) 
        with self.assertRaises(TypeError) as context:
            obtained = sd + 1
        # Compare calculated and expected criterion
        self.assertTrue(TypeError)

    def test_externalmutation(self):
        sd = SignalDetection(1, 1, 2, 1)
        sd.hits = 2
        sd.misses = 3
        sd.fa = 4
        sd.cr = 5
        print(sd.hits)
        expected = SignalDetection(1, 1, 2, 1).criterion()
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertEqual(obtained, expected)
        
    def test_corruption(self):
        sd = SignalDetection(1, 1, 2, 1)
        sd_dp = sd.d_prime()
        sd.h_rate = sd.h_rate + 0.1
        
        
        
    def test_multiplication(self):
        sd = SignalDetection(1, 2, 3, 1) * 4
        expected = SignalDetection(4, 8, 12, 4).criterion()
        obtained = sd.criterion()
        # Compare calculated and expected criterion
        self.assertEqual(obtained, expected)

if __name__ == '__main__':
    unittest.main()
