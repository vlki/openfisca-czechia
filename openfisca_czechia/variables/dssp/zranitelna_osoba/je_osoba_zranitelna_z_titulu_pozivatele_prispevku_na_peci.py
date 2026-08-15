from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_pozivatele_prispevku_na_peci(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu poživatele příspěvku na péči v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        # § 7 odst. 1 g) Zranitelnou osobou je poživatel příspěvku na péči ve stupni II nebo vyšším
        # TODO
        return False
