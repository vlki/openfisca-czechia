from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class vyjimka_z_minimalniho_zdravotniho_pojisteni(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    default_value = False
    label = "Výjimka z minimálního zdravotního pojištění"
