from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class uplatnuje_danove_zvyhodneni_na_vyzivovane_deti(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    default_value = False
    label = "Zda osoba uplatňuje daňové zvýhodnění na vyživované děti"
    documentation = """
    Daňové zvýhodnění lze uplatnit jen u zaměstnavatele, u kterého je podepsané
    prohlášení k dani, a v rámci domácnosti jen u jednoho z rodičů.
    """
