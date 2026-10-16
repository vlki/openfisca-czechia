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
            # Pracovní příjem vstupuje do součtu omezený zdola na nule, protože
            # podle § 4 odst. 3 zákona 151/2025 Sb. nelze žádný z příjmů snížit
            # o ztrátu z jiného druhu příjmů
            suma_pro_domacnost_bez_nezaopat_deti(
                "dssp_zapocitatelny_pracovni_prijem_osoby"
            )
            + suma_pro_domacnost_bez_nezaopat_deti("starobni_duchod")
            + suma_pro_domacnost_bez_nezaopat_deti("invalidni_vdovecky_sirotci_duchody")
            + suma_pro_domacnost_bez_nezaopat_deti("materska")
            + suma_pro_domacnost_bez_nezaopat_deti("nemocenska")
            + suma_pro_domacnost_bez_nezaopat_deti("odmena_pestouna")
            + suma_pro_domacnost_bez_nezaopat_deti("podpora_v_nezamestnanosti")
            + suma_pro_domacnost_bez_nezaopat_deti("rodicovsky_prispevek")
            + suma_pro_domacnost_bez_nezaopat_deti("vyzivne_na_deti")
            + suma_pro_domacnost_bez_nezaopat_deti("jine_prijmy")
        )
