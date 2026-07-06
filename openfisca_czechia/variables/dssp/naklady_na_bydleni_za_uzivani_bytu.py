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

        uhrazene_najemne = najem + poplatky

        byt_nebo_dum = typ_bydleni == TypBydleni.byt_nebo_rodinny_dum
        jiny_prostor = typ_bydleni == TypBydleni.jiny_nez_obytny_prostor
        vlastni = vztah_k_nemovitosti == VztahKNemovitosti.vlastni_druzstevni_sluzebni
        najemni = vztah_k_nemovitosti == VztahKNemovitosti.najemni_podnajemni

        podminky_s_vypocty_nakladu = [
            # §23 odst. 1
            (
                byt_nebo_dum & vlastni,
                vlastnicky_pausal,
            ),
            # §23 odst. 3
            (
                byt_nebo_dum & najemni,
                min_(uhrazene_najemne, normativni_najemne),
            ),
            # §24 odst. 1
            (
                jiny_prostor & vlastni,
                0.8 * vlastnicky_pausal,
            ),
            # §24 odst. 2 a §25
            (
                (jiny_prostor & najemni)
                | (typ_bydleni == TypBydleni.pobytove_sluzby)
                | (typ_bydleni == TypBydleni.ubytovaci_zarizeni),
                # TODO: move 0.8 to parameter
                min_(uhrazene_najemne, 0.8 * normativni_najemne),
            ),
        ]
        cast_za_uzivani_bytu = select(*zip(*podminky_s_vypocty_nakladu), default=0.0)

        # Část za energie: nad hranicí příjmu paušál, pod ní skutečné
        # náklady, nejvýše 1,2násobek paušálu
        # TODO: move 1.43 and 1.2 to parameters
        cast_za_energie = where(
            rozhodny_prijem >= 1.43 * zivotni_minimum,  # noqa: PLR2004
            energeticky_pausal,
            min_(naklady_na_energie, 1.2 * energeticky_pausal),
        )

        return cast_za_uzivani_bytu + cast_za_energie
