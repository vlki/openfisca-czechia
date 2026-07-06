from openfisca_core.model_api import select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_castka_na_nezaopatrene_dite(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Částka na nezaopatřené dítě ve výpočtu výše bonusu na dítě v rámci DSSP"

    def formula(domacnost, period, parameters):
        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        zivotni_minimum = domacnost("zivotni_minimum_domacnosti", period)
        vsechny_osoby_zranitelne = domacnost(
            "dssp_jsou_vsechny_osoby_v_domacnosti_zranitelne", period
        )

        parametry_castky = parameters(period).dssp.castka_na_nezaopatrene_dite

        hranice_1 = (
            parametry_castky.hranice_jako_nasobky_zivotniho_minima_domacnosti.hranice_1
            * zivotni_minimum
        )
        hranice_2 = (
            parametry_castky.hranice_jako_nasobky_zivotniho_minima_domacnosti.hranice_2
            * zivotni_minimum
        )
        hranice_3 = (
            parametry_castky.hranice_jako_nasobky_zivotniho_minima_domacnosti.hranice_3
            * zivotni_minimum
        )

        castka_na_nezaopatrene_dite = select(
            [
                rozhodny_prijem <= hranice_1,
                rozhodny_prijem < hranice_2,
                rozhodny_prijem <= hranice_3,
            ],
            [
                # výpočet pro podmínku rozhodny_prijem <= hranice_1
                where(
                    vsechny_osoby_zranitelne,
                    parametry_castky.castky_mezi_hranicemi.castka_pod_hranici_1_pro_zranitelne,
                    parametry_castky.castky_mezi_hranicemi.castka_pod_hranici_1_pro_nezranitelne,
                ),
                # výpočet pro podmínku rozhodny_prijem < hranice_2
                parametry_castky.castky_mezi_hranicemi.castka_pod_hranici_2,
                # výpočet pro podmínku rozhodny_prijem <= hranice_3
                (
                    parametry_castky.castky_mezi_hranicemi.zakladni_castka_pod_hranici_3_ktera_se_snizuje_koeficientem
                    * (4 - (rozhodny_prijem / zivotni_minimum))
                ),
            ],
            default=0.0,
        )

        return castka_na_nezaopatrene_dite
