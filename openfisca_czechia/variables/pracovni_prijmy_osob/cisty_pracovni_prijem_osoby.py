from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class cisty_pracovni_prijem_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Čistý pracovní příjem osoby"

    def formula(person, period, parameters):
        hruby_prijem_z_hlavniho_zamestnani = person(
            "hruby_prijem_z_hlavniho_zamestnani", period
        )
        dpfo_z_hlavniho_zamestnani = person("dpfo_z_hlavniho_zamestnani", period)
        socialni_z_hlavniho_zamestnani = person(
            "odvod_socialniho_pojisteni_zamestnance_z_hlavniho_zamestnani", period
        )
        zdravotni_z_hlavniho_zamestnani = person(
            "odvod_zdravotniho_pojisteni_zamestnance_z_hlavniho_zamestnani", period
        )

        return (
            hruby_prijem_z_hlavniho_zamestnani
            - dpfo_z_hlavniho_zamestnani
            - socialni_z_hlavniho_zamestnani
            - zdravotni_z_hlavniho_zamestnani
        )
