from openfisca_core.model_api import select
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class je_samoplatce_zdravotniho_pojisteni(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Zda má osoba povinnost sama platit zdravotní pojištění"

    def formula(osoba, period, parameters):
        plati_zdravotni_u_nektereho_zamestnani = False
        for index in INDEXY_ZAMESTNANI:
            hruby_prijem = osoba(f"hruby_prijem_ze_zamestnani_{index}", period)
            povinnost_odvodu = osoba(
                f"povinnost_odvodu_zdravotniho_pojisteni_ze_zamestnani_{index}", period
            )
            plati_zdravotni_u_nektereho_zamestnani = (
                plati_zdravotni_u_nektereho_zamestnani
                | ((hruby_prijem > 0) & povinnost_odvodu)
            )

        plati_stat_zdravotni_pojisteni = osoba("plati_stat_zdravotni_pojisteni", period)
        je_registrovana_na_uradu_prace = osoba("je_registrovana_na_uradu_prace", period)

        return select(
            [
                plati_zdravotni_u_nektereho_zamestnani,
                plati_stat_zdravotni_pojisteni,
                je_registrovana_na_uradu_prace,
            ],
            [
                # pro podminku plati_zdravotni_u_nektereho_zamestnani
                False,
                # pro podminku plati_stat_zdravotni_pojisteni
                False,
                # pro podminku je_registrovana_na_uradu_prace
                False,
            ],
            # Pouze pokud neplati zadna z podminek vyse, tak je osoba samoplatce
            default=True,
        )
