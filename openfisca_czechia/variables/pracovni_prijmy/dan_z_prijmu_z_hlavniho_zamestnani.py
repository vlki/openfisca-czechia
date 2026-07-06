from openfisca_core.model_api import max_, min_
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dan_z_prijmu_z_hlavniho_zamestnani(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daň z příjmu z hlavního zaměstnání"

    def formula(person, period, parameters):
        hruby_prijem = person("hruby_prijem_z_hlavniho_zamestnani", period)

        prumerna_hruba_mesicni_mzda_predchozi_rok = parameters(
            period.last_year
        ).prumerna_hruba_mesicni_mzda
        hranice_vyssi_sazby_dane = parameters(
            period
        ).dan_z_prijmu_fyzickych_osob.hranice_vyssi_sazby

        hranice_vyssi_sazby_dane_jako_rocni_castka = (
            hranice_vyssi_sazby_dane * prumerna_hruba_mesicni_mzda_predchozi_rok
        )
        hranice_vyssi_sazby_dane_jako_mesicni_castka = (
            hranice_vyssi_sazby_dane_jako_rocni_castka / 12
        )

        cast_prijmu_pod_hranici = min_(
            hruby_prijem, hranice_vyssi_sazby_dane_jako_mesicni_castka
        )
        cast_prijmu_nad_hranici = max_(
            hruby_prijem - hranice_vyssi_sazby_dane_jako_mesicni_castka, 0
        )

        dan_z_prijmu_danena_zakladni_sazbou = (
            cast_prijmu_pod_hranici
            * parameters(period).dan_z_prijmu_fyzickych_osob.zakladni_sazba
        )
        dan_z_prijmu_danena_vyssi_sazbou = (
            cast_prijmu_nad_hranici
            * parameters(period).dan_z_prijmu_fyzickych_osob.vyssi_sazba
        )

        return dan_z_prijmu_danena_zakladni_sazbou + dan_z_prijmu_danena_vyssi_sazbou
