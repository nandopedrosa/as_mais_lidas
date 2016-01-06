"""
unittests.py: Application unit tests

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
from src.ns import news_source_national
from src.utils import util


class NewsSourceNationalTests(unittest.TestCase):
    def test_g1(self):
        news, title = news_source_national.get_most_read('g1')
        self.assertEqual(len(news), 5)

    def test_uol(self):
        news, title = news_source_national.get_most_read('uol')
        self.assertEqual(len(news), 5)

    def test_r7(self):
        news, title = news_source_national.get_most_read('r7')
        self.assertEqual(len(news), 7)

    def test_folha(self):
        news, title = news_source_national.get_most_read('folha')
        self.assertEqual(len(news), 5)

    def test_bol(self):
        news, title = news_source_national.get_most_read('bol')
        self.assertEqual(len(news), 5)

    def test_carta(self):
        news, title = news_source_national.get_most_read('carta')
        self.assertEqual(len(news), 5)

    def test_veja(self):
        news, title = news_source_national.get_most_read('veja')
        self.assertEqual(len(news), 10)

    def test_local_df(self):
        news, title = news_source_national.get_most_read('localDF')
        self.assertEqual(len(news), 4)

    def test_local_sp(self):
        news, title = news_source_national.get_most_read('localSP')
        self.assertEqual(len(news), 5)

    def test_local_rj(self):
        news, title = news_source_national.get_most_read('localRJ')
        self.assertEqual(len(news), 5)

    def test_getstate(self):
        state = util.getstate('187.111.96.65')
        self.assertEqual('RJ', state)

        state = util.getstate('177.166.105.8')
        self.assertEqual('SP', state)

        state = util.getstate('189.9.21.1')
        self.assertEqual('DF', state)


if __name__ == '__main__':
    unittest.main()
