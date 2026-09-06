from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class cisty_pracovni_prijem_osoby_bez_danoveho_bonusu(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Čistý pracovní příjem osoby bez daňového bonusu"

    def formula(osoba, period, parameters):
        cisty_pracovni_prijem_osoby = osoba("cisty_pracovni_prijem_osoby", period)
        danovy_bonus_osoby = osoba("danovy_bonus_osoby", period)

        return cisty_pracovni_prijem_osoby - danovy_bonus_osoby
