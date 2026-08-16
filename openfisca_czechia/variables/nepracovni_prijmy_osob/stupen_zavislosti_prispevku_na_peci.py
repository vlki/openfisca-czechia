from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class StupenZavislostiPrispevkuNaPeci(Enum):
    stupen_1 = "I. Lehká závislost"
    stupen_2 = "II. Středně těžká závislost"
    stupen_3 = "III. Těžká závislost"
    stupen_4 = "IV. Úplná závislost"


class stupen_zavislosti_prispevku_na_peci(Variable):
    value_type = Enum
    possible_values = StupenZavislostiPrispevkuNaPeci
    default_value = StupenZavislostiPrispevkuNaPeci.stupen_1
    entity = Osoba
    definition_period = MONTH
    label = "Stupeň závislosti příspěvku na péči"
