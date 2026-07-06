from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná v rámci DSSP"
    definition_period = MONTH
