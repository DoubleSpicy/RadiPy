# unit tests
import unittest
import radipy

class TestModels(unittest.TestCase):
    def test_gEUD(self):
        model = radipy.models.gEUD([1, 2, 3], [4, 5, 6], 2)
        self.assertAlmostEqual(model.val, 5.385164807, places=3)

    def test_LKB(self):
        model = radipy.models.LKB(1, 1, [1, 2, 3], [4, 5, 6], 2)
        model.gEUD_model.val = 1
        model.compute()
        self.assertAlmostEqual(model.val[0], 1.25331413, places=3)

    def test_RS(self):
        model = radipy.models.RS([1,2], [1,2], 1, 1, 1)
        self.assertAlmostEqual(model.val, 0.9000016934, places=3)

if __name__ == '__main__':
    unittest.main()

