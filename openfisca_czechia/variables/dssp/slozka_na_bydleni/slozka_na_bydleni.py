from openfisca_core.model_api import max_
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_slozka_na_bydleni(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Složka DSSP na bydlení"

    def formula(domacnost, period, parameters):
        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        zivotni_minimum = domacnost("zivotni_minimum_domacnosti", period)
        rozhodne_naklady_na_bydleni = domacnost(
            "dssp_naklady_na_bydleni_za_uzivani_bytu", period
        )

        parametry_slozky = parameters(period).dssp.slozka_na_bydleni

        # Částka, o kterou rozhodný příjem převyšuje definovaný násobek životního minima domácnosti
        # (dle zákona 151/2025 § 19 odst. 3)
        castka_o_kterou_rozhodny_prijem_prevysuje = max_(
            rozhodny_prijem
            - (
                parametry_slozky.nasobek_zivotniho_minima_domacnosti_jako_hranice_pro_rozhodny_prijem_nad_kterou_se_pricita_k_urcene_casti_rozhodneho_prijmu
                * zivotni_minimum
            ),
            0,
        )

        # Určená část rozhodného příjmu jako součet dvou částí: první je násobek rozhodného příjmu definovaným
        # koeficientem a druhá násobek výše počítané převyšující částky definovaný druhým koeficientem (dle
        # zákona 151/2025 § 19 odst. 2 a 3)
        urcena_cast_rozhodneho_prijmu = (
            parametry_slozky.koeficient_pro_vypocet_urcene_casti_rozhodneho_prijmu
            * rozhodny_prijem
        ) + (
            parametry_slozky.koeficient_jako_nasobek_castky_presujici_hranici_nasobku_zivotniho_minima_ktery_se_pricita_k_urcene_casti_rozhodneho_prijmu
            * castka_o_kterou_rozhodny_prijem_prevysuje
        )

        # Výše složky na bydlení je rozdíl mezi rozhodnými náklady na bydlení a určenou částí rozhodného
        # příjmu (dle zákona 151/2025 § 34 odst. 1). Zároveň určená část rozhodného příjmu nesmí být vyšší
        # než rozhodné náklady na bydlení (dle zákona 151/2025 § 19 odst. 1), proto nastavujeme, že nejníže
        # může být výše složky 0.
        return max_(rozhodne_naklady_na_bydleni - urcena_cast_rozhodneho_prijmu, 0)
