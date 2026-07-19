from openfisca_core.model_api import select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_energeticky_pausal_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Energetický paušál domácnosti v rámci DSSP"

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

        energeticky_pausal_domacnosti = parameters(period).dssp.energeticky_pausal[
            klic_velikosti_domacnosti
        ]
        nasobek_energetickeho_pausalu_pro_zranitelne = parameters(
            period
        ).dssp.energeticky_pausal_pro_zranitelne

        energeticky_pausal_domacnosti = energeticky_pausal_domacnosti * where(
            vsechny_osoby_zranitelne,
            nasobek_energetickeho_pausalu_pro_zranitelne,
            1,
        )

        return energeticky_pausal_domacnosti
