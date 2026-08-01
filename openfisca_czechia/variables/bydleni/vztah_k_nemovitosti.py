from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class VztahKNemovitosti(Enum):
    __order__ = "vlastni_druzstevni_sluzebni najemni_podnajemni"
    vlastni_druzstevni_sluzebni = "Vlastní/družstevní/služební"
    najemni_podnajemni = "Nájemní/podnájemní"


class vztah_k_nemovitosti(Variable):
    value_type = Enum
    possible_values = VztahKNemovitosti
    default_value = VztahKNemovitosti.vlastni_druzstevni_sluzebni
    entity = Domacnost
    definition_period = MONTH
    label = "Vztah domácnosti k nemovitosti"
