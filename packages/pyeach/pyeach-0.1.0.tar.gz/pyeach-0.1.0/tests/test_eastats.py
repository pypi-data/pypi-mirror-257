import pandas as pd
import unittest
from pyeach import eastats

class TestEAStats(unittest.TestCase):
    def test_ci_int(self):
        self.assertEqual(eastats.ci_int(pd.Series([0,1])), (-3.9923217661378816, 4.992321766137882))
        self.assertEqual(eastats.ci_int(pd.Series([0,1]), distr="bin"), (0.0, 1.0))

    def test_mean_t_test(self):
        self.assertEqual(eastats.mean_t_test(pd.Series([0,1]), 1), 0.42264973081037427)

    def test_geo_mean(self):
        self.assertEqual(eastats.geo_mean(pd.Series([0,2])), 0.0)
        self.assertEqual(eastats.geo_mean(pd.Series([0,2]), include_zeros=False), 2.0)
        self.assertEqual(eastats.geo_mean(pd.Series([1,2])), 1.414213562373095)

    def test_smape(self):
        self.assertEqual(eastats.smape(pd.Series([1,2]), pd.Series([2,4])), 0.3333333333333333)

if __name__ == '__main__':
    unittest.main()
