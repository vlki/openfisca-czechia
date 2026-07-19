from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class DsspVelikostObceBydliste(Enum):
    __order__ = "obec_do_69999_obyvatel obec_70000_obyvatel_a_vice praha_a_brno"
    obec_do_69999_obyvatel = "Obec do 69 999 obyvateli"
    obec_70000_obyvatel_a_vice = "Obec s alespoň 70 000 obyvateli"
    praha_a_brno = "Praha a Brno"


class dssp_velikost_obce_bydliste(Variable):
    value_type = Enum
    possible_values = DsspVelikostObceBydliste
    default_value = DsspVelikostObceBydliste.praha_a_brno
    entity = Domacnost
    definition_period = MONTH
    label = "Velikost obce bydliště pro DSSP"
