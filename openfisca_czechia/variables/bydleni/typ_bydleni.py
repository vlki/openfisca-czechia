from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class TypBydleni(Enum):
    __order__ = "byt_nebo_rodinny_dum ubytovaci_zarizeni pobytove_sluzby jiny_nez_obytny_prostor"
    byt_nebo_rodinny_dum = "Byt nebo rodinný dům"
    ubytovaci_zarizeni = "Ubytovací zařízení"
    pobytove_sluzby = "Pobytové služby"
    jiny_nez_obytny_prostor = "Jiný než obytný prostor"


class typ_bydleni(Variable):
    value_type = Enum
    possible_values = TypBydleni
    default_value = TypBydleni.byt_nebo_rodinny_dum
    entity = Domacnost
    definition_period = MONTH
    label = "Typ bydlení"
