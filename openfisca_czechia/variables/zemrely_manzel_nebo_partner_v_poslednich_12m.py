from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class zemrely_manzel_nebo_partner_v_poslednich_12m(Variable):
    value_type = bool
    entity = Osoba
    label = "Zemřelý manžel nebo partner v posledních 12 měsících"
    definition_period = MONTH
    default_value = False
