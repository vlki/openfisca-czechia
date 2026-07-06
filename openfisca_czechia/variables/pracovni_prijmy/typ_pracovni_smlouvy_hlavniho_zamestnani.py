from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class TypPracovniSmlouvy(Enum):
    __order__ = "hpp dpp dpc"
    hpp = "Hlavní pracovní poměr"
    dpp = "Dohoda o provedení práce"
    dpc = "Dohoda o pracovní činnosti"


class typ_pracovni_smlouvy_hlavniho_zamestnani(Variable):
    value_type = Enum
    possible_values = TypPracovniSmlouvy
    default_value = TypPracovniSmlouvy.hpp
    entity = Osoba
    definition_period = MONTH
    # TODO:
    label = ""
