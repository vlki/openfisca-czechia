from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_rozhodny_prijem(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Rozhodný příjem pro DSSP"

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

        return (
            suma_pro_domacnost_bez_nezaopat_deti("cisty_prijem_osoby")
            + suma_pro_domacnost_bez_nezaopat_deti("duchody")
            + suma_pro_domacnost_bez_nezaopat_deti("materska")
            + suma_pro_domacnost_bez_nezaopat_deti("nemocenska")
            + suma_pro_domacnost_bez_nezaopat_deti("odmena_pestouna")
            + suma_pro_domacnost_bez_nezaopat_deti("podpora_v_nezamestnanosti")
            + suma_pro_domacnost_bez_nezaopat_deti("prispevek_na_uhradu_potreb_na_dite")
            + suma_pro_domacnost_bez_nezaopat_deti("rodicovsky_prispevek")
            + suma_pro_domacnost_bez_nezaopat_deti("vyzivne_na_deti")
            + suma_pro_domacnost_bez_nezaopat_deti("jine_prijmy")
        )
