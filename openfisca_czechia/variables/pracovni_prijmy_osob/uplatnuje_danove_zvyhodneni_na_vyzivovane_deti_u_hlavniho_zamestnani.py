from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class uplatnuje_danove_zvyhodneni_na_vyzivovane_deti_u_hlavniho_zamestnani(Variable):
    value_type = bool
    entity = Osoba
    label = (
        "Zda osoba uplatňuje daňové zvýhodnění na vyživované děti u hlavního zaměstnání"
    )
    definition_period = MONTH
    default_value = False
