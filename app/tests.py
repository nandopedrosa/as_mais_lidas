"""
tests.py: Application unit tests

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
import app.news_source_national as news_source_national
import app.news_source_international as news_source_international
from app.aml_utils import getstate


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

    def test_local_pe(self):
        news, title = news_source_national.get_most_read('localPE')
        self.assertEqual(len(news), 5)

    def test_local_ac(self):
        news, title = news_source_national.get_most_read('localAC')
        self.assertEqual(len(news), 5)

    def test_local_al(self):
        news, title = news_source_national.get_most_read('localAL')
        self.assertEqual(len(news), 5)

    def test_local_ap(self):
        news, title = news_source_national.get_most_read('localAP')
        self.assertEqual(len(news), 5)

    def test_local_am(self):
        news, title = news_source_national.get_most_read('localAM')
        self.assertEqual(len(news), 6)

    def test_local_ba(self):
        news, title = news_source_national.get_most_read('localBA')
        self.assertEqual(len(news), 5)

    def test_local_ce(self):
        news, title = news_source_national.get_most_read('localCE')
        self.assertEqual(len(news), 5)

    def test_local_es(self):
        news, title = news_source_national.get_most_read('localES')
        self.assertEqual(len(news), 5)

    def test_local_go(self):
        news, title = news_source_national.get_most_read('localGO')
        self.assertEqual(len(news), 5)

    def test_local_ma(self):
        news, title = news_source_national.get_most_read('localMA')
        self.assertEqual(len(news), 6)

    def test_local_mt(self):
        news, title = news_source_national.get_most_read('localMT')
        self.assertEqual(len(news), 5)

    def test_local_ms(self):
        news, title = news_source_national.get_most_read('localMS')
        self.assertEqual(len(news), 5)

    def test_local_mg(self):
        news, title = news_source_national.get_most_read('localMG')
        self.assertEqual(len(news), 4)

    def test_local_pa(self):
        news, title = news_source_national.get_most_read('localPA')
        self.assertEqual(len(news), 5)

    def test_local_pb(self):
        news, title = news_source_national.get_most_read('localPB')
        self.assertEqual(len(news), 5)

    def test_local_pr(self):
        news, title = news_source_national.get_most_read('localPR')
        self.assertEqual(len(news), 5)

    def test_local_pi(self):
        news, title = news_source_national.get_most_read('localPI')
        self.assertEqual(len(news), 5)

    def test_local_rn(self):
        news, title = news_source_national.get_most_read('localRN')
        self.assertEqual(len(news), 5)

    def test_local_rs(self):
        news, title = news_source_national.get_most_read('localRS')
        self.assertEqual(len(news), 5)

    def test_local_sc(self):
        news, title = news_source_national.get_most_read('localSC')
        self.assertEqual(len(news), 4)

    def test_local_ro(self):
        news, title = news_source_national.get_most_read('localRO')
        self.assertEqual(len(news), 5)

    def test_local_rr(self):
        news, title = news_source_national.get_most_read('localRR')
        self.assertEqual(len(news), 5)

    def test_local_se(self):
        news, title = news_source_national.get_most_read('localSE')
        self.assertEqual(len(news), 5)

    def test_local_to(self):
        news, title = news_source_national.get_most_read('localTO')
        self.assertEqual(len(news), 5)

    def test_ny(self):
        news, title = news_source_international.get_most_read('ny')
        self.assertEqual(len(news), 10)

    def test_wp(self):
        news, title = news_source_international.get_most_read('wp')
        self.assertEqual(len(news), 5)

    def test_tg(self):
        news, title = news_source_international.get_most_read('tg')
        self.assertEqual(len(news), 10)

    def test_lf(self):
        news, title = news_source_international.get_most_read('lf')
        self.assertEqual(len(news), 5)

    def test_tt(self):
        news, title = news_source_international.get_most_read('tt')
        self.assertEqual(len(news), 10)

    def test_ep(self):
        news, title = news_source_international.get_most_read('ep')
        self.assertEqual(len(news), 10)

    def test_getstate(self):
        state = getstate('187.111.96.65')
        self.assertEqual('RJ', state)

        state = getstate('177.166.105.8')
        self.assertEqual('SP', state)

        state = getstate('189.9.21.1')
        self.assertEqual('DF', state)


if __name__ == '__main__':
    unittest.main()
