"""
test_entertainment.py: Application unit tests for the Entertainment Category.

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import app.news_source_entertainment as nse


class SportsTests(unittest.TestCase):
    def test_ego(self):
        news, title = nse.get_most_read('en_ego')
        self.assertEqual(len(news), 9)

    def test_fuxico(self):
        news, title = nse.get_most_read('en_fuxico')
        self.assertEqual(len(news), 10)

    def test_contigo(self):
        news, title = nse.get_most_read('en_contigo')
        self.assertEqual(len(news), 5)

    def test_tititi(self):
        news, title = nse.get_most_read('en_tititi')
        self.assertEqual(len(news), 5)

    def test_vip(self):
        news, title = nse.get_most_read('en_vip')
        self.assertEqual(len(news), 5)

if __name__ == '__main__':
    unittest.main()
