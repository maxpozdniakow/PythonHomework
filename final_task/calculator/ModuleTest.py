from calculator.pycalc import  basic_operators,compound_operators, priority_dict, good_chars
from math import *
import math as mt
import unittest

class ModuleTest(unittest.TestCase):

	def calc(st):
		return calculator(st, mt, basic_operators, compound_operators, priority_dict, good_chars))
					 
    def test(self):
        self.assertEqual(calc('--+-5'), --+-5)
        self.assertEqual(calc('+10-.4'), +10-.4)
        self.assertEqual(calc('--------1'), 1)
        self.assertFalse(calc('5-1==4+2+3-7'))
        self.assertEqual(calc('1^3^5'), 1**3**5)
        self.assertEqual(calc('pow(8,3)'), pow(8, 3))
		self.assertEqual(calc('pow(1, 0)'), pow(1, 0))
        self.assertEqual(calc('log(e,e)'), log(e, e))
        self.assertEqual(calc('factorial(11)'), factorial(11))