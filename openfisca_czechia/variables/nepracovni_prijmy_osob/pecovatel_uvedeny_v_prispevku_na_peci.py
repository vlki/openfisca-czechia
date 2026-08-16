from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class pecovatel_uvedeny_v_prispevku_na_peci(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    default_value = False
    label = "Pečovatel uvedený v příspěvku na péči, pečující o dítě ve věku do 10 let závislé ve stupni I. nebo o osobu závislou ve stupni II. nebo vyšším"
