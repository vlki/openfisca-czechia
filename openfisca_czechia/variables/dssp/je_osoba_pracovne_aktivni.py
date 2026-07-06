from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_pracovne_aktivni(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba pracovně aktivní v rámci DSSP"
    definition_period = MONTH
