from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class nazev_zamestnavatele_zamestnani_1(Variable):
    value_type = str
    entity = Osoba
    definition_period = MONTH
    default_value = ""
    label = "Název zaměstnavatele prvního zaměstnání"
    documentation = """
    Pouze popisek pro zobrazení, do výpočtu nevstupuje. Identita zaměstnavatele,
    podle které se příjmy seskupují, je v proměnné zamestnavatel_zamestnani_1.

    Záměrně tu není max_length: s ním numpy hodnoty drží jako bytes a porovnání
    s Python stringem pak tiše vrací False.
    """
