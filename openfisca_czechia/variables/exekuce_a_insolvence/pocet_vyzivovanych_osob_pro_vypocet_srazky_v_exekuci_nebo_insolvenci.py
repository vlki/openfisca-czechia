from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class pocet_vyzivovanych_osob_pro_vypocet_srazky_v_exekuci_nebo_insolvenci(Variable):
    value_type = int
    default_value = 0
    entity = Osoba
    definition_period = MONTH
    label = "Počet vyživovaných osob pro výpočet srážky v exekuci nebo insolvenci"
