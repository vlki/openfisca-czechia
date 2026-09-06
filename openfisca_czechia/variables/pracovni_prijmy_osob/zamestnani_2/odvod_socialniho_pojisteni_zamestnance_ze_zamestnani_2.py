import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class odvod_socialniho_pojisteni_zamestnance_ze_zamestnani_2(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Výše odvodu sociálního pojištění zaměstnance z druhého zaměstnání"

    def formula(osoba, period, parameters):
        povinnost_odvodu = osoba(
            "povinnost_odvodu_socialniho_pojisteni_ze_zamestnani_2", period
        )
        hruby_prijem = osoba("hruby_prijem_ze_zamestnani_2", period)

        sazba_zamestnance = parameters(
            period
        ).socialni_pojisteni.sazby.sazba_zamestnance

        return where(
            povinnost_odvodu,
            # Zaokrouhluje se na koruny nahoru. Nejdřív děláme round na 2 desetinná
            # místa, aby se odstranily artefakty po násobení Python float čísel
            np.ceil(np.round(hruby_prijem * sazba_zamestnance, decimals=2)),
            0.0,
        )
