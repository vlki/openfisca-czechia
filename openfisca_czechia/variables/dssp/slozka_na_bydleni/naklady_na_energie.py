from openfisca_core.model_api import select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_naklady_na_energie(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Náklady domácnosti na energie pro účely DSSP"

    def formula(domacnost, period, parameters):
        naklady_na_energie = domacnost("naklady_na_energie", period)
        vyuziva_domacnost_tuha_paliva = domacnost(
            "vyuziva_domacnost_tuha_paliva", period
        )

        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        hranice_rozhodneho_prijmu_pro_tuha_paliva = 1.43 * domacnost(
            "zivotni_minimum_domacnosti", period
        )
        rozhodny_prijem_pod_hranici_pro_tuha_paliva = (
            rozhodny_prijem < hranice_rozhodneho_prijmu_pro_tuha_paliva
        )

        pocet_osob = domacnost(
            "dssp_pocet_osob_v_domacnosti_pro_vypocet_nakladu_na_bydleni", period
        )
        klic_velikosti_domacnosti = select(
            [
                pocet_osob <= 1,
                pocet_osob == 2,  # noqa: PLR2004
                pocet_osob == 3,  # noqa: PLR2004
                pocet_osob == 4,  # noqa: PLR2004
                pocet_osob >= 5,  # noqa: PLR2004
            ],
            [
                "jednoclenna_domacnost",
                "dvouclenna_domacnost",
                "triclenna_domacnost",
                "ctyrclenna_domacnost",
                "peti_nebo_viceclenna_domacnost",
            ],
            default="",
        )
        naklady_na_energie_tuha_paliva = parameters(
            period
        ).dssp.naklady_na_energie_spojene_s_uzivanim_tuhych_paliv[
            klic_velikosti_domacnosti
        ]

        return where(
            vyuziva_domacnost_tuha_paliva & rozhodny_prijem_pod_hranici_pro_tuha_paliva,
            naklady_na_energie + naklady_na_energie_tuha_paliva,
            naklady_na_energie,
        )
