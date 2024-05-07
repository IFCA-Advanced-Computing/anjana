import pandas as pd
from anjana import anonymity
from anjana.anonymity import utils
import pycanon
from copy import copy
import numpy as np


class TestAdult:
    data = pd.read_csv("./examples/data/adult.csv")  # 32561 rows
    data.columns = data.columns.str.strip()
    cols = [
        "workclass",
        "education",
        "marital-status",
        "occupation",
        "sex",
        "native-country",
    ]
    for col in cols:
        data[col] = data[col].str.strip()

    quasi_ident = [
        "age",
        "education",
        "marital-status",
        "occupation",
        "sex",
        "native-country",
    ]
    ident = ["race"]
    sens_att = "salary-class"
    k = 10
    l_div = 2
    c_div = 2
    t = 0.5
    alpha = 0.8
    beta = 0.5
    delta = 0.4
    supp_level = 50

    hierarchies = {
        "age": dict(pd.read_csv("./examples/hierarchies/age.csv", header=None)),
        "education": dict(
            pd.read_csv("./examples/hierarchies/education.csv", header=None)
        ),
        "marital-status": dict(
            pd.read_csv("./examples/hierarchies/marital.csv", header=None)
        ),
        "occupation": dict(
            pd.read_csv("./examples/hierarchies/occupation.csv", header=None)
        ),
        "sex": dict(pd.read_csv("./examples/hierarchies/sex.csv", header=None)),
        "native-country": dict(
            pd.read_csv("./examples/hierarchies/country.csv", header=None)
        ),
    }

    def test_supp_ident(self):
        data_anon = anonymity.utils.suppress_identifiers(self.data, self.ident)
        data_anon_real = copy(self.data)
        data_anon_real["race"] = "*"
        assert data_anon_real.equals(data_anon)

    def test_k_anon(self):
        data_anon = anonymity.k_anonymity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.k,
            self.supp_level,
            self.hierarchies,
        )
        assert self.k <= pycanon.anonymity.k_anonymity(data_anon, self.quasi_ident)

    def test_k_anon_100sup(self):
        data_anon = anonymity.k_anonymity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.k,
            100,
            self.hierarchies,
        )
        assert self.k <= pycanon.anonymity.k_anonymity(data_anon, self.quasi_ident)

    def test_l_div(self):
        data_anon = anonymity.l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.l_div,
            self.supp_level,
            self.hierarchies,
        )
        assert self.l_div <= pycanon.anonymity.l_diversity(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_t_closs(self):
        data_anon = anonymity.t_closeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.t,
            self.supp_level,
            self.hierarchies,
        )
        assert self.t >= pycanon.anonymity.t_closeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_alpha_k_anon(self):
        data_anon = anonymity.alpha_k_anonymity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.alpha,
            self.supp_level,
            self.hierarchies,
        )
        alpha, k = pycanon.anonymity.alpha_k_anonymity(
            data_anon, self.quasi_ident, [self.sens_att]
        )
        assert self.alpha >= alpha and self.k <= k

    def test_basic_beta(self):
        data_anon = anonymity.basic_beta_likeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.beta,
            self.supp_level,
            self.hierarchies,
        )
        assert self.beta >= pycanon.anonymity.basic_beta_likeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_enhanced_beta(self):
        data_anon = anonymity.enhanced_beta_likeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.beta,
            self.supp_level,
            self.hierarchies,
        )
        assert self.beta >= pycanon.anonymity.enhanced_beta_likeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_delta_disclosure(self):
        data_anon = anonymity.delta_disclosure(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.delta,
            self.supp_level,
            self.hierarchies,
        )
        assert self.delta >= pycanon.anonymity.delta_disclosure(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_entropy_l(self):
        data_anon = anonymity.entropy_l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.l_div,
            self.supp_level,
            self.hierarchies,
        )
        assert len(data_anon) == 0

    def test_rec_c_l(self):
        data_anon = anonymity.recursive_c_l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.l_div,
            self.c_div,
            self.supp_level,
            self.hierarchies,
        )
        assert len(data_anon) == 0

    def test_basic_beta0(self):
        data_anon = anonymity.basic_beta_likeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            0,
            self.supp_level,
            self.hierarchies,
        )
        assert 0 == pycanon.anonymity.basic_beta_likeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_enhanced_beta0(self):
        data_anon = anonymity.enhanced_beta_likeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            0,
            self.supp_level,
            self.hierarchies,
        )
        assert 0 == pycanon.anonymity.enhanced_beta_likeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_basic_beta10(self):
        data_anon = anonymity.basic_beta_likeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            10,
            self.supp_level,
            self.hierarchies,
        )
        assert 10 >= pycanon.anonymity.basic_beta_likeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_enhanced_beta10(self):
        data_anon = anonymity.enhanced_beta_likeness(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            10,
            self.supp_level,
            self.hierarchies,
        )
        assert 10 >= pycanon.anonymity.enhanced_beta_likeness(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_delta0(self):
        data_anon = anonymity.delta_disclosure(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            0,
            self.supp_level,
            self.hierarchies,
        )
        assert 0 == pycanon.anonymity.delta_disclosure(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_delta10(self):
        data_anon = anonymity.delta_disclosure(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            10,
            self.supp_level,
            self.hierarchies,
        )
        assert 10 >= pycanon.anonymity.delta_disclosure(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_l_div_k1(self):
        data_anon = anonymity.l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            1,
            self.l_div,
            self.supp_level,
            self.hierarchies,
        )
        assert self.l_div <= pycanon.anonymity.l_diversity(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_l_div1(self):
        data_anon = anonymity.l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            1,
            self.supp_level,
            self.hierarchies,
        )
        assert 1 <= pycanon.anonymity.l_diversity(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_entropy_l_div1(self):
        data_anon = anonymity.entropy_l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            1,
            self.supp_level,
            self.hierarchies,
        )
        assert 1 <= pycanon.anonymity.entropy_l_diversity(
            data_anon, self.quasi_ident, [self.sens_att]
        )

    def test_rec_c1_l_div2(self):
        data_anon = anonymity.recursive_c_l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            1,
            2,
            self.supp_level,
            self.hierarchies,
        )
        c_cal, l_cal = pycanon.anonymity.recursive_c_l_diversity(
            data_anon, self.quasi_ident, [self.sens_att]
        )
        assert 1 <= c_cal and 1 <= l_cal


class TestHospital:
    data = pd.read_csv("./examples/data/hospital_extended.csv")

    ident = ["name"]
    quasi_ident = ["age", "gender", "city"]
    sens_att = "disease"
    k = 2
    l_div = 2
    supp_level = 0
    hierarchies = {
        "age": dict(pd.read_csv("./examples/hierarchies/age.csv", header=None)),
        "gender": {
            0: data["gender"].values,
            1: np.array(["*"] * len(data["gender"].values)),
        },
        "city": {0: data["city"].values, 1: np.array(["*"] * len(data["city"].values))},
    }

    def test_k_anon(self):
        data_anon = anonymity.k_anonymity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.k,
            self.supp_level,
            self.hierarchies,
        )

        data_anon_real = copy(self.data)
        data_anon_real[self.ident] = "*"
        hierarchy_age = self.hierarchies["age"]
        pos = []
        for elem in data_anon_real["age"].values:
            pos.append(np.where(hierarchy_age[0].values == elem)[0][0])
        data_anon_real["age"] = hierarchy_age[2].values[pos]
        assert data_anon_real.equals(data_anon)

    def test_l_div(self):
        data_anon = anonymity.l_diversity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.sens_att,
            self.k,
            self.l_div,
            self.supp_level,
            self.hierarchies,
        )

        data_anon_real = copy(self.data)
        data_anon_real[self.ident] = "*"
        hierarchy_age = self.hierarchies["age"]
        pos = []
        for elem in data_anon_real["age"].values:
            pos.append(np.where(hierarchy_age[0].values == elem)[0][0])
        data_anon_real["age"] = hierarchy_age[2].values[pos]
        data_anon_real["city"] = "*"
        assert data_anon_real.equals(data_anon)

    def test_get_transformation(self):
        data_anon = anonymity.k_anonymity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.k,
            self.supp_level,
            self.hierarchies,
        )

        transformation = utils.get_transformation(
            data_anon, self.quasi_ident, self.hierarchies
        )
        assert [2, 0, 0] == transformation

    def test_get_transformation_2qi(self):
        hierarchies = {
            "age": dict(pd.read_csv("./examples/hierarchies/age.csv", header=None)),
            "city": {
                0: self.data["city"].values,
                1: np.array(["*"] * len(self.data["city"].values)),
            },
        }
        data_anon = anonymity.k_anonymity(
            self.data,
            self.ident,
            self.quasi_ident,
            self.k,
            self.supp_level,
            hierarchies,
        )

        transformation = utils.get_transformation(
            data_anon, self.quasi_ident, self.hierarchies
        )
        assert [2, 0, 0] == transformation
