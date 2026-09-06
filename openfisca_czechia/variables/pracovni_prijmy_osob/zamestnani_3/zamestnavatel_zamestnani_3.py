from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.zamestnavatel import (
    Zamestnavatel,
)


class zamestnavatel_zamestnani_3(Variable):
    value_type = Enum
    possible_values = Zamestnavatel
    default_value = Zamestnavatel.zamestnavatel_c
    entity = Osoba
    definition_period = MONTH
    label = "Zaměstnavatel třetího zaměstnání"
    documentation = """
    Identita zaměstnavatele. Podle ní se příjmy seskupují pro limity odvodů,
    pro srážkovou daň a pro výpočet zálohy na daň. Ve výchozím stavu má každé
    zaměstnání jiného zaměstnavatele. Pokud jsou dvě zaměstnání u téhož
    zaměstnavatele, je potřeba jim nastavit stejnou hodnotu.
    """
