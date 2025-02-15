import unittest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arithmetic import BCHGenerator, signedMod

class TestBCHGenerator(unittest.TestCase):
    
    def test_all_zeros(self):
        d = [0] * 12
        expected = [0] * 12 + [
            signedMod((4*0 + 10*0 + 3*0 + 0 + 5*0 + 16*0 + 0 + 12*0 + 16*0 + 14*0 + 7*0 + 13*0), 17),
            signedMod((2*0 + 15*0 + 15*0 + 16*0 + 15*0 + 9*0 + 12*0 + 4*0 + 16*0 + 11*0 + 3*0 + 6*0), 17),
            signedMod((3*0 + 11*0 + 16*0 + 4*0 + 12*0 + 9*0 + 15*0 + 16*0 + 15*0 + 15*0 + 2*0 + 13*0), 17),
            signedMod((7*0 + 14*0 + 16*0 + 12*0 + 0 + 16*0 + 5*0 + 0 + 3*0 + 10*0 + 4*0 + 0), 17)
        ]
        self.assertEqual(BCHGenerator(d), expected)
    
    def test_all_ones(self):
        d = [1] * 12
        expected = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            signedMod((4*1 + 10*1 + 3*1 + 1 + 5*1 + 16*1 + 1 + 12*1 + 16*1 + 14*1 + 7*1 + 13*1), 17),
            signedMod((2*1 + 15*1 + 15*1 + 16*1 + 15*1 + 9*1 + 12*1 + 4*1 + 16*1 + 11*1 + 3*1 + 6*1), 17),
            signedMod((3*1 + 11*1 + 16*1 + 4*1 + 12*1 + 9*1 + 15*1 + 16*1 + 15*1 + 15*1 + 2*1 + 13*1), 17),
            signedMod((7*1 + 14*1 + 16*1 + 12*1 + 1 + 16*1 + 5*1 + 1 + 3*1 + 10*1 + 4*1 + 1), 17)
        ]
        self.assertEqual(BCHGenerator(d), expected)
    
    def test_incremental_values(self):
        d = list(range(12))
        expected = [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            signedMod((4*0 + 10*1 + 3*2 + 3 + 5*4 + 16*5 + 6 + 12*7 + 16*8 + 14*9 + 7*10 + 13*11), 17),
            signedMod((2*0 + 15*1 + 15*2 + 16*3 + 15*4 + 9*5 + 12*6 + 4*7 + 16*8 + 11*9 + 3*10 + 6*11), 17),
            signedMod((3*0 + 11*1 + 16*2 + 4*3 + 12*4 + 9*5 + 15*6 + 16*7 + 15*8 + 15*9 + 2*10 + 13*11), 17),
            signedMod((7*0 + 14*1 + 16*2 + 12*3 + 4 + 16*5 + 5*6 + 7 + 3*8 + 10*9 + 4*10 + 11), 17)
        ]
        self.assertEqual(BCHGenerator(d), expected)
    
    def test_negative_values(self):
        d = [-1] * 12
        expected = [
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            signedMod((4*(-1) + 10*(-1) + 3*(-1) + (-1) + 5*(-1) + 16*(-1) + (-1) + 12*(-1) + 16*(-1) + 14*(-1) + 7*(-1) + 13*(-1)), 17),
            signedMod((2*(-1) + 15*(-1) + 15*(-1) + 16*(-1) + 15*(-1) + 9*(-1) + 12*(-1) + 4*(-1) + 16*(-1) + 11*(-1) + 3*(-1) + 6*(-1)), 17),
            signedMod((3*(-1) + 11*(-1) + 16*(-1) + 4*(-1) + 12*(-1) + 9*(-1) + 15*(-1) + 16*(-1) + 15*(-1) + 15*(-1) + 2*(-1) + 13*(-1)), 17),
            signedMod((7*(-1) + 14*(-1) + 16*(-1) + 12*(-1) + (-1) + 16*(-1) + 5*(-1) + (-1) + 3*(-1) + 10*(-1) + 4*(-1) + (-1)), 17)
        ]
        self.assertEqual(BCHGenerator(d), expected)
    
    def test_input_length_error(self):
        d = [1] * 13  # Invalid length
        with self.assertRaises(ValueError):
            BCHGenerator(d)
    
    def test_non_integer_input(self):
        d = [1] * 12
        d[0] = "string"  # Invalid type
        with self.assertRaises(TypeError):
            BCHGenerator(d)

    def test_repeated_pattern(self):
        d = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
        expected = [
            1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
            signedMod((4*1 + 10*2 + 3*3 + 1 + 5*2 + 16*3 + 1 + 12*2 + 16*3 + 14*1 + 7*2 + 13*3), 17),
            signedMod((2*1 + 15*2 + 15*3 + 16*1 + 15*2 + 9*3 + 12*1 + 4*2 + 16*3 + 11*1 + 3*2 + 6*3), 17),
            signedMod((3*1 + 11*2 + 16*3 + 4*1 + 12*2 + 9*3 + 15*1 + 16*2 + 15*3 + 15*1 + 2*2 + 13*3), 17),
            signedMod((7*1 + 14*2 + 16*3 + 12*1 + 1 + 16*2 + 5*3 + 1 + 3*1 + 10*2 + 4*3 + 3), 17)
        ]
        self.assertEqual(BCHGenerator(d), expected)

if __name__ == '__main__':
    unittest.main()
