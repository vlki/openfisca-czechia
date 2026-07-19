from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_pracovni_bonus(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Pracovní bonus v rámci DSSP"

    def formula(domacnost, period, parameters):
        slozka_na_bydleni = domacnost("dssp_slozka_na_bydleni", period)
        slozka_na_zivobyti = domacnost("dssp_slozka_na_zivobyti", period)
        bonus_na_dite = domacnost("dssp_bonus_na_dite", period)

        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        zivotni_minimum = domacnost("zivotni_minimum_domacnosti", period)
        prijem_zohlednovany_pro_bonus = domacnost(
            "dssp_prijem_zohlednovany_pro_pracovni_bonus", period
        )

        parametry_bonusu = parameters(period).dssp.pracovni_bonus

        hranice_delici_vypocty_bonusu = (
            parametry_bonusu.nasobek_zivotniho_minima_domacnosti_jako_hranice_rozhodneho_prijmu_delici_vypocty_pracovniho_bonusu
        ) * zivotni_minimum

        pracovni_bonus_v_situaci_pod_hranici = (
            parametry_bonusu.pracovni_bonus_jako_cast_prijmu_v_situaci_pod_hranici
            * prijem_zohlednovany_pro_bonus
        )

        zakladni_cast_pro_vypocet_bonusu_v_situaci_nad_hranici = (
            parametry_bonusu.cast_kladneho_rozdilu_prijmu_a_rozhodneho_prijmu_prevysujiciho_hranici_jako_zakladni_cast_pro_vypocet_bonusu
            * (
                prijem_zohlednovany_pro_bonus
                - (rozhodny_prijem - hranice_delici_vypocty_bonusu)
            )
        )
        redukcni_cast_pro_vypocet_bonusu_v_situaci_nad_hranici = (
            parametry_bonusu.cast_rozhodneho_prijmu_prevysujiciho_hranici_jako_redukcni_cast_pro_vypocet_bonusu
            * (rozhodny_prijem - hranice_delici_vypocty_bonusu)
        )

        # Pokud redukční část převyšuje základní část, pak je výše pracovního bonusu 0 Kč
        pracovni_bonus_v_situaci_nad_hranici = max(
            (
                zakladni_cast_pro_vypocet_bonusu_v_situaci_nad_hranici
                - redukcni_cast_pro_vypocet_bonusu_v_situaci_nad_hranici
            ),
            0,
        )

        pracovni_bonus = where(
            rozhodny_prijem <= hranice_delici_vypocty_bonusu,
            pracovni_bonus_v_situaci_pod_hranici,
            pracovni_bonus_v_situaci_nad_hranici,
        )

        nenulova_slozka_na_bydleni = slozka_na_bydleni > 0
        nenulova_slozka_na_zivobyti = slozka_na_zivobyti > 0
        nenulovy_bonus_na_dite = bonus_na_dite > 0
        nenulovy_prijem_zohlednovany_pro_pracovni_bonus = (
            prijem_zohlednovany_pro_bonus > 0
        )

        # Pracovní bonus je součástí dávky pouze pokud má alespoň jeden z členů domácnosti příjem
        # zohledňovaný pro pracovní bonus a alespoň jedna z ostatních částek dávky je vyšší než 0 Kč.
        # (dle zákona 151/2025 § 40 odst. 1)
        return where(
            (
                nenulovy_prijem_zohlednovany_pro_pracovni_bonus
                & (
                    nenulova_slozka_na_bydleni
                    | nenulova_slozka_na_zivobyti
                    | nenulovy_bonus_na_dite
                )
            ),
            pracovni_bonus,
            0,
        )
