from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_slozka_na_zivobyti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Složka DSSP na živobytí"

    def formula(domacnost, period, parameters):
        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        zivotni_minimum = domacnost("zivotni_minimum_domacnosti", period)
        soucet_castek_na_zivotni_potreby = domacnost(
            "dssp_soucet_castek_na_zivotni_potreby_clenu_domacnosti", period
        )

        parametry_slozky = parameters(period).dssp.slozka_na_zivobyti

        hranice_rozhodneho_prijmu_pod_kterou_je_slozka_soucasti_davky = (
            parametry_slozky.nasobek_zivotniho_minima_domacnosti_jako_hranice_rozhodneho_prijmu_pod_kterou_je_slozka_soucasti_davky
        ) * zivotni_minimum

        rozhodny_prijem_po_odecteni_casti = rozhodny_prijem - (
            rozhodny_prijem
            * parametry_slozky.odecitany_nasobek_rozhodneho_prijmu_ve_vypoctu
        )

        return where(
            (
                rozhodny_prijem
                <= hranice_rozhodneho_prijmu_pod_kterou_je_slozka_soucasti_davky
            ),
            soucet_castek_na_zivotni_potreby - rozhodny_prijem_po_odecteni_casti,
            0,
        )
