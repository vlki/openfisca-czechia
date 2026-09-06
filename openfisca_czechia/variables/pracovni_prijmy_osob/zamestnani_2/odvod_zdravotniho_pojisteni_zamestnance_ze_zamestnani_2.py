import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class odvod_zdravotniho_pojisteni_zamestnance_ze_zamestnani_2(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Výše odvodu zdravotního pojištění zaměstnance z druhého zaměstnání"
    documentation = """
    Bez dopočtu do minimálního vyměřovacího základu. Ten se posuzuje za všechna
    zaměstnání dohromady, a je proto na úrovni osoby v proměnné
    doplatek_do_minimalniho_zdravotniho_pojisteni.
    """

    def formula(osoba, period, parameters):
        povinnost_odvodu = osoba(
            "povinnost_odvodu_zdravotniho_pojisteni_ze_zamestnani_2", period
        )
        hruby_prijem = osoba("hruby_prijem_ze_zamestnani_2", period)

        sazba_zamestnance = parameters(
            period
        ).zdravotni_pojisteni.sazby.sazba_zamestnance

        return where(
            povinnost_odvodu,
            # Zaokrouhluje se na koruny nahoru. Nejdřív děláme round na 2 desetinná
            # místa, aby se odstranily artefakty po násobení Python float čísel
            np.ceil(np.round(hruby_prijem * sazba_zamestnance, decimals=2)),
            0.0,
        )
