from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class navazuje_rodicovsky_prispevek_na_materskou(Variable):
    value_type = bool
    entity = Osoba
    label = "Navazuje rodičovský příspěvek na peněžitou pomoc v mateřství (mateřskou)"
    definition_period = MONTH
    default_value = True
