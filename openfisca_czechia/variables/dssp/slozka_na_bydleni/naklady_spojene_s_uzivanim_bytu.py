from openfisca_core.model_api import select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_naklady_spojene_s_uzivanim_bytu(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Náklady domácnosti spojené s uživáním bytu v rámci DSSP"

    def formula(domacnost, period, parameters):
        pocet_osob = domacnost(
            "dssp_pocet_osob_v_domacnosti_pro_vypocet_nakladu_na_bydleni", period
        )
        vsechny_osoby_zranitelne = domacnost(
            "dssp_jsou_vsechny_osoby_v_domacnosti_zranitelne", period
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

        naklady_pro_zranitelne = parameters(
            period
        ).dssp.naklady_spojene_s_uzivanim_bytu_pro_zranitelne[klic_velikosti_domacnosti]
        naklady_pro_nezranitelne = parameters(
            period
        ).dssp.naklady_spojene_s_uzivanim_bytu[klic_velikosti_domacnosti]

        return where(
            vsechny_osoby_zranitelne,
            naklady_pro_zranitelne,
            naklady_pro_nezranitelne,
        )
