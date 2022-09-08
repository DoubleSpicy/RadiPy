# unit tests
import unittest
import radipy

class TestModels(unittest.TestCase):
    def test_gEUD(self):
        model = radipy.models.gEUD([1, 2, 3], [4, 5, 6], 2)
        self.assertEqual(model.val, 1024)

    def test_LKB(self):
        gEUD = radipy.models.gEUD([1, 2, 3], [4, 5, 6], 2)
        gEUD.val = 1 # mockup val
        model = radipy.models.LKB(1, 1, gEUD)
        self.assertAlmostEqual(model.val[0], 1.2533141373154997)

    def test_RS(self):
        model = radipy.models.RS([1,2], [1,2], 1, 1, 1)
        self.assertAlmostEqual(model.val, 0.9000016934, places=3)

if __name__ == '__main__':
    unittest.main()

