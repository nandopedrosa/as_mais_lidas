"""
test_technology.py: Application unit tests for the Technology Category.

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import news_source_technology as nst


class TechTests(unittest.TestCase):
    def test_g1(self):
        news, title = nst.get_most_read('tec_g1')
        self.assertEqual(len(news), 5)

    def test_giz(self):
        news, title = nst.get_most_read('tec_giz')
        self.assertEqual(len(news), 15)

    def test_cw(self):
        news, title = nst.get_most_read('tec_cw')
        self.assertEqual(len(news), 4)

    # def test_olhar(self):
    # news, title = nst.get_most_read('tec_olhar')
    # self.assertEqual(len(news), 9)

    def test_canal(self):
        news, title = nst.get_most_read('tec_canal')
        self.assertEqual(len(news), 9)

        # def test_uol(self):
        # news, title = nst.get_most_read('tec_uol')
        # self.assertEqual(len(news), 5)


if __name__ == '__main__':
    unittest.main()
