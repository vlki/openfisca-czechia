import numpy as np

from openfisca_core.model_api import max_, min_
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dpfo_z_hlavniho_zamestnani_pred_uplatnenim_slev(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daň z příjmu fyzických osob z hlavního zaměstnání před uplatněním slev"

    def formula(person, period, parameters):
        hruby_prijem = person("hruby_prijem_z_hlavniho_zamestnani", period)

        # Základ daně se zaokrouhluje na celé 100 nahoru
        zaklad_dane = np.ceil(hruby_prijem / 100) * 100

        prumerna_hruba_mesicni_mzda_predchozi_rok = parameters(
            period.last_year
        ).prumerna_hruba_mesicni_mzda

        parametry_sazeb = parameters(period).dpfo.sazby

        hranice_vyssi_sazby_dane_jako_rocni_castka = (
            parametry_sazeb.hranice_vyssi_sazby
            * prumerna_hruba_mesicni_mzda_predchozi_rok
        )
        hranice_vyssi_sazby_dane_jako_mesicni_castka = (
            hranice_vyssi_sazby_dane_jako_rocni_castka / 12
        )

        cast_prijmu_pod_hranici = min_(
            zaklad_dane, hranice_vyssi_sazby_dane_jako_mesicni_castka
        )
        cast_prijmu_nad_hranici = max_(
            zaklad_dane - hranice_vyssi_sazby_dane_jako_mesicni_castka, 0
        )

        dan_z_prijmu_danena_zakladni_sazbou = (
            cast_prijmu_pod_hranici * parametry_sazeb.zakladni_sazba
        )
        dan_z_prijmu_danena_vyssi_sazbou = (
            cast_prijmu_nad_hranici * parametry_sazeb.vyssi_sazba
        )

        # Daň se zaokrouhluje na celé koruny nahoru. Nejdříve děláme zaokrouhlení na
        # 2 desetinná místa, abychom odstranili artefakty po násobení floatů v Pythonu.
        dpfo = np.ceil(
            np.round(
                dan_z_prijmu_danena_zakladni_sazbou + dan_z_prijmu_danena_vyssi_sazbou,
                decimals=2,
            )
        )

        return dpfo
