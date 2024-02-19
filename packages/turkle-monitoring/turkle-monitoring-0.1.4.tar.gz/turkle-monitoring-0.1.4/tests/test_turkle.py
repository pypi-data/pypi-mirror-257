import unittest
from turkle import turkle
import pandas as pd

class TestTurkle(unittest.TestCase):

  def setUp(self):

    ref_data = {
      "label" : [0,1,0,1,0,0,0,1],
      "predicted_probability" : [0.1,0.8,0.3,0.7,0.12,0.6,0.5,0.9],
      "credit_score" : [610, 608, 612, 615, 600, 614, 620, 630],
      "timestamp" : ["2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06", "2022-07", "2022-08"],
      "feature_a" : [23, 25, 21, 28, 30, 29, 24, 21]
      }
    
    prod_data = {
      "label" : [0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1],
      "predicted_probability" : [0.1,0.8,0.3,0.7,0.12,0.6,0.5,0.9, 0.1,0.8,0.3,0.7,0.12,0.6,0.5,0.9],
      "credit_score" : [610, 608, 612, 615, 600, 614, 620, 630, 610, 608, 612, 615, 600, 614, 620, 630],
      "timestamp" : ["2023-01", "2023-01", "2023-01", "2023-02", "2023-02", "2023-02", "2023-03", "2023-03", "2023-03", "2023-04", "2023-04", "2023-04", "2023-05", "2023-05", "2023-05", "2023-05"],
      "feature_a" : [23, 25, 21, 28, 30, 29, 24, 21, 23, 27, 27, 28, 27, 29, 24, 21]
      }
    
    ref_df = pd.DataFrame(data=ref_data)
    prod_df = pd.DataFrame(data=prod_data)

    bin_edges = {"feature_a" : [20,23,25,28,30]}

    self.model = turkle.Model(ref_df, prod_df, bin_edges)

  def test_feature_drift(self):

    result = self.model.feature_drift(plot=False, return_data=True)
    
    assert(result["total_psi"][0], 0.22)


  def test_concept_drift(self):
    result = self.model.concept_drift(plot=False, return_data=True)

    assert(result["2023-01"][0], 0.0417)



if __name__ == '__main__':
    unittest.main()