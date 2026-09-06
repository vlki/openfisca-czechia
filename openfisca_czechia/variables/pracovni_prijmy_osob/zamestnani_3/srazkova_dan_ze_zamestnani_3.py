import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class srazkova_dan_ze_zamestnani_3(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Srážková daň z příjmu z třetího zaměstnání"

    def formula(osoba, period, parameters):
        podleha_srazkove_dani = osoba(
            "podleha_prijem_ze_zamestnani_3_srazkove_dani", period
        )
        hruby_prijem = osoba("hruby_prijem_ze_zamestnani_3", period)

        sazba_srazkove_dane = parameters(period).dpfo.sazby.zvlastni_sazba_srazkove_dane

        # Základ daně i sražená daň se podle § 36 odst. 3 zaokrouhlují na celé
        # koruny dolů. Před zaokrouhlením daně děláme round na 2 desetinná místa,
        # aby se odstranily artefakty po násobení Python float čísel.
        zaklad_dane = np.floor(hruby_prijem)
        srazkova_dan = np.floor(np.round(zaklad_dane * sazba_srazkove_dane, decimals=2))

        return where(podleha_srazkove_dani, srazkova_dan, 0.0)
