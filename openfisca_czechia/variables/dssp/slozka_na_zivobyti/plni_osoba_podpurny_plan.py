from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_plni_osoba_podporny_plan(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda plní osoba podpůrný plán v rámci DSSP"
    definition_period = MONTH
    # Předpokládáme, že osoby plní ve většině případů podpůrný plán, proto default_value = True
    default_value = True
