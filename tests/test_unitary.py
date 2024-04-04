import unittest
from anjana import anonymity
import pandas as pd
import beartype


class TestInvalidValues(unittest.TestCase):
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
        "sex": dict(pd.read_csv("../examples/hierarchies/sex.csv", header=None)),
        "native-country": dict(
            pd.read_csv("./examples/hierarchies/country.csv", header=None)
        ),
    }

    def test_k_neg(self):
        k = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                k,
                supp_level,
                self.hierarchies,
            )

    def test_k_0(self):
        k = 0
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                k,
                supp_level,
                self.hierarchies,
            )

    def test_alpha_neg(self):
        k = -1
        alpha = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.alpha_k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                alpha,
                supp_level,
                self.hierarchies,
            )

    def test_alpha_high(self):
        k = 0
        alpha = 1.5
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.alpha_k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                alpha,
                supp_level,
                self.hierarchies,
            )

    def test_supp_level_neg(self):
        k = 1
        supp_level = -10
        with self.assertRaises(ValueError):
            anonymity.k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                k,
                supp_level,
                self.hierarchies,
            )

    def test_supp_level_high(self):
        k = 1
        supp_level = 110
        with self.assertRaises(ValueError):
            anonymity.k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                k,
                supp_level,
                self.hierarchies,
            )

    def test_l_neg(self):
        k = 1
        l_div = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_l_0(self):
        k = 1
        l_div = 0
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_ent_l_neg(self):
        k = 1
        l_div = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.entropy_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_ent_l_0(self):
        k = 1
        l_div = 0
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.entropy_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_rec_l_neg(self):
        k = 1
        l_div = -1
        c = 1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.recursive_c_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                c,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_rec_l_0(self):
        k = 1
        l_div = 0
        c = 1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.recursive_c_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                c,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_rec_c_neg(self):
        k = 1
        l_div = 1
        c = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.recursive_c_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                c,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_rec_c_0(self):
        k = 1
        l_div = 1
        c = 0
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.recursive_c_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                c,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_t_neg(self):
        k = 1
        t = -1.5
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.t_closeness(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                t,
                supp_level,
                self.hierarchies,
            )

    def test_t_high(self):
        k = 1
        t = 1.5
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.t_closeness(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                t,
                supp_level,
                self.hierarchies,
            )

    def test_basic_beta_neg(self):
        k = 1
        beta = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.basic_beta_likeness(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                beta,
                supp_level,
                self.hierarchies,
            )

    def test_enhanced_beta_neg(self):
        k = 1
        beta = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.enhanced_beta_likeness(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                beta,
                supp_level,
                self.hierarchies,
            )

    def test_delta_neg(self):
        k = 1
        delta = -1
        supp_level = 50
        with self.assertRaises(ValueError):
            anonymity.delta_disclosure(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                delta,
                supp_level,
                self.hierarchies,
            )

    def test_kanon_data(self):
        k = 1
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.k_anonymity(
                "data.csv",
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                supp_level,
                self.hierarchies,
            )

    def test_kanon_float(self):
        k = 1.5
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                supp_level,
                self.hierarchies,
            )

    def test_alpha_kanon_float(self):
        k = 1.5
        alpha = 0.5
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.k_anonymity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                alpha,
                supp_level,
                self.hierarchies,
            )

    def test_ldiv_float(self):
        k = 2
        l_div = 1.5
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_entropy_ldiv_float(self):
        k = 2
        l_div = 1.5
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.entropy_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_rec_ldiv_float(self):
        k = 2
        c = 1
        l_div = 1.5
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.recursive_c_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                c,
                l_div,
                supp_level,
                self.hierarchies,
            )

    def test_rec_c_ldiv_float(self):
        k = 2
        c = 1.5
        l_div = 1
        supp_level = 50
        with self.assertRaises(beartype.roar.BeartypeCallHintParamViolation):
            anonymity.recursive_c_l_diversity(
                self.data,
                self.ident,
                self.quasi_ident,
                self.sens_att,
                k,
                c,
                l_div,
                supp_level,
                self.hierarchies,
            )
