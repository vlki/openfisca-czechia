from openfisca_core.model_api import min_, select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost
from openfisca_czechia.variables.bydliste.typ_bydleni import TypBydleni
from openfisca_czechia.variables.bydliste.vztah_k_nemovitosti import VztahKNemovitosti


class dssp_naklady_na_bydleni_za_uzivani_bytu(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Náklady domácnosti na bydlení za užívání bytu v rámci DSSP"

    def formula(domacnost, period, parameters):
        typ_bydleni = domacnost("typ_bydleni", period)
        vztah_k_nemovitosti = domacnost("vztah_k_nemovitosti", period)

        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        zivotni_minimum = domacnost("zivotni_minimum_domacnosti", period)
        energeticky_pausal = domacnost("dssp_energeticky_pausal_domacnosti", period)
        naklady_na_energie = domacnost("dssp_naklady_na_energie", period)
        vlastnicky_pausal = domacnost("dssp_vlastnicky_pausal_domacnosti", period)
        normativni_najemne = domacnost("dssp_normativni_najemne_domacnosti", period)
        najem = domacnost("naklady_na_najemne", period)
        poplatky = domacnost("dalsi_poplatky_spojene_s_bydlenim", period)

        parametry_nakladu = parameters(
            period
        ).dssp.slozka_na_bydleni.naklady_na_bydleni_za_uzivani_bytu

        uhrazene_najemne = najem + poplatky

        byt_nebo_dum = typ_bydleni == TypBydleni.byt_nebo_rodinny_dum
        jiny_prostor = typ_bydleni == TypBydleni.jiny_nez_obytny_prostor
        vlastni = vztah_k_nemovitosti == VztahKNemovitosti.vlastni_druzstevni_sluzebni
        najemni = vztah_k_nemovitosti == VztahKNemovitosti.najemni_podnajemni

        podminky_s_vypocty_nakladu = [
            # § 23 odst. 1
            (
                byt_nebo_dum & vlastni,
                vlastnicky_pausal,
            ),
            # § 23 odst. 3
            (
                byt_nebo_dum & najemni,
                min_(uhrazene_najemne, normativni_najemne),
            ),
            # § 24 odst. 1
            (
                jiny_prostor & vlastni,
                0.8 * vlastnicky_pausal,
            ),
            # § 24 odst. 2
            (
                (jiny_prostor & najemni) | (typ_bydleni == TypBydleni.pobytove_sluzby),
                min_(
                    uhrazene_najemne,
                    (
                        parametry_nakladu.podil_normativniho_najemneho_jako_maximum_zapocitane_vyse_najemneho_pro_jine_prostory_k_bydleni
                        * normativni_najemne,
                    ),
                ),
            ),
            # § 25
            (
                typ_bydleni == TypBydleni.ubytovaci_zarizeni,
                min_(
                    uhrazene_najemne,
                    (
                        parametry_nakladu.podil_normativniho_najemneho_jako_maximum_zapocitane_vyse_najemneho_pro_ubytovaci_zarizeni
                        * normativni_najemne,
                    ),
                ),
            ),
        ]
        cast_za_uzivani_bytu = select(*zip(*podminky_s_vypocty_nakladu), default=0.0)

        hranice_nad_kterou_se_zapocitava_pausal = (
            parametry_nakladu.nasobek_zivotniho_minima_domacnosti_jako_hranice_rozhodneho_prijmu_nad_kterou_se_pro_energie_zapocitava_pausal
            * zivotni_minimum
        )
        maximum_zapocitane_vyse_nakladu_na_energie = (
            parametry_nakladu.nasobek_energetickeho_pausalu_jako_maximum_zapocitane_vyse_skutecnych_nakladu_na_energie
            * energeticky_pausal
        )

        # Část za energie: nad hranicí příjmu paušál, pod ní skutečné
        # náklady, nejvýše Xnásobek paušálu
        cast_za_energie = where(
            rozhodny_prijem >= hranice_nad_kterou_se_zapocitava_pausal,
            energeticky_pausal,
            min_(naklady_na_energie, maximum_zapocitane_vyse_nakladu_na_energie),
        )

        return cast_za_uzivani_bytu + cast_za_energie
