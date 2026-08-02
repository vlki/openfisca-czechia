from openfisca_core.model_api import select
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class je_samoplatce_zdravotniho_pojisteni(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Zda má osoba povinnost sama platit zdravotní pojištění"

    def formula(osoba, period, parameters):
        hruby_prijem_z_hlavniho_zamestnani = osoba(
            "hruby_prijem_z_hlavniho_zamestnani", period
        )
        povinnost_odvodu_zdravotniho_pojisteni_z_hlavniho_zamestnani = osoba(
            "povinnost_odvodu_zdravotniho_pojisteni_z_hlavniho_zamestnani", period
        )

        plati_zdravotni_u_hlavniho_zamestnani = (
            hruby_prijem_z_hlavniho_zamestnani > 0
        ) & povinnost_odvodu_zdravotniho_pojisteni_z_hlavniho_zamestnani

        plati_stat_zdravotni_pojisteni = osoba("plati_stat_zdravotni_pojisteni", period)
        je_registrovana_na_uradu_prace = osoba("je_registrovana_na_uradu_prace", period)

        return select(
            [
                plati_zdravotni_u_hlavniho_zamestnani,
                plati_stat_zdravotni_pojisteni,
                je_registrovana_na_uradu_prace,
            ],
            [
                # pro podminku plati_zdravotni_u_hlavniho_zamestnani
                False,
                # pro podminku plati_stat_zdravotni_pojisteni
                False,
                # pro podminku je_registrovana_na_uradu_prace
                False,
            ],
            # Pouze pokud neplati zadna z podminek vyse, tak je osoba samoplatce
            default=True,
        )
