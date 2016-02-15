"""
test_news.py: Application unit tests for the Sports Category.

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import app.news_source_sports as nss


class SportsTests(unittest.TestCase):
    def test_espn(self):
        news, title = nss.get_most_read('e_espn_br')
        self.assertEqual(len(news), 6)


if __name__ == '__main__':
    unittest.main()
