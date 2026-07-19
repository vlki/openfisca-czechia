from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class cisty_prijem_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Čistý příjem osoby"

    def formula(person, period, parameters):
        hruby_prijem_z_hlavniho_zamestnani = person(
            "hruby_prijem_z_hlavniho_zamestnani", period
        )
        dpfo_z_hlavniho_zamestnani = person("dpfo_z_hlavniho_zamestnani", period)

        return hruby_prijem_z_hlavniho_zamestnani - dpfo_z_hlavniho_zamestnani
