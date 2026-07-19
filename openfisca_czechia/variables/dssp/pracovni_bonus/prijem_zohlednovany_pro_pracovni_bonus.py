from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_prijem_zohlednovany_pro_pracovni_bonus(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Příjem zohledňovaný pro pracovní bonus DSSP"

    def formula(domacnost, period, parameters):
        nezaopat_deti_v_domacnosti = domacnost.members("je_nezaopatrene_dite", period)

        def suma_pro_domacnost_bez_nezaopat_deti(nazev_prijmove_promenne):
            hodnoty_prijmove_promenne = domacnost.members(
                nazev_prijmove_promenne, period
            )
            hodnoty_prijmove_promenne_bez_nezaopat_deti = where(
                nezaopat_deti_v_domacnosti, 0, hodnoty_prijmove_promenne
            )
            return domacnost.sum(hodnoty_prijmove_promenne_bez_nezaopat_deti)

        rodicovske_prispevky_osob = domacnost.members("rodicovsky_prispevek", period)
        osoby_s_navazujici_rodicovskou_na_materskou = domacnost.members(
            "navazuje_rodicovsky_prispevek_na_materskou", period
        )

        rodicovske_prispevky_jen_navazujici_na_materskou_a_bez_nezaopat_deti = where(
            osoby_s_navazujici_rodicovskou_na_materskou & ~nezaopat_deti_v_domacnosti,
            rodicovske_prispevky_osob,
            0,
        )

        return (
            suma_pro_domacnost_bez_nezaopat_deti("cisty_prijem_osoby")
            + suma_pro_domacnost_bez_nezaopat_deti("nemocenska")
            + suma_pro_domacnost_bez_nezaopat_deti("odmena_pestouna")
            + domacnost.sum(
                rodicovske_prispevky_jen_navazujici_na_materskou_a_bez_nezaopat_deti
            )
        )
