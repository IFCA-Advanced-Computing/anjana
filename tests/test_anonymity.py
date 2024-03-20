import pandas as pd
from anjana import anonymity
import pycanon


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
