from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class vyse_pojistneho_pro_samoplatce_zdravotniho_pojisteni(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Výše pojistného pro samoplátce zdravotního pojištění"

    def formula(osoba, period, parameters):
        minimalni_mzda = parameters(period).minimalni_mzda
        sazba_samoplatce = parameters(period).zdravotni_pojisteni.sazby.sazba_samoplatce

        return minimalni_mzda * sazba_samoplatce
