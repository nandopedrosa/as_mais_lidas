"""
test_technology.py: Application unit tests for the Technology Category.

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import news_source_technology as nst


class SportsTests(unittest.TestCase):
    def test_g1(self):
        news, title = nst.get_most_read('tec_g1')
        self.assertEqual(len(news), 5)


if __name__ == '__main__':
    unittest.main()
