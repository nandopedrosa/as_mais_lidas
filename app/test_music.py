"""
test_entertainment.py: Application unit tests for the Music Category.

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import app.news_source_music as nsm


class SportsTests(unittest.TestCase):
    def test_rs(self):
        news, title = nsm.get_most_read('m_rs')
        self.assertEqual(len(news), 5)

    def test_whiplash(self):
        news, title = nsm.get_most_read('m_whiplash')
        self.assertEqual(len(news), 10)


if __name__ == '__main__':
    unittest.main()
