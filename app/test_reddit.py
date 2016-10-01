"""
test_reddit.py: Application unit tests for the Reddit Category.

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import news_source_reddit as nsr


class RedditTests(unittest.TestCase):
    def test_ask(self):
        news, title = nsr.get_most_read('re_ask')
        self.assertEqual(len(news), 5)


if __name__ == '__main__':
    unittest.main()
