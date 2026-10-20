from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class prijem_osoby_pro_vypocet_srazky_v_exekuci_nebo_insolvenci(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Příjem osoby pro výpočet srážky v exekuci nebo insolvenci"

    def formula(osoba, period, parameters):
        cisty_pracovni_prijem_osoby_bez_danoveho_bonusu = osoba(
            "cisty_pracovni_prijem_osoby_bez_danoveho_bonusu", period
        )
        rodicovsky_prispevek = osoba("rodicovsky_prispevek", period)
        starobni_duchod = osoba("starobni_duchod", period)
        invalidni_vdovecky_sirotci_duchody = osoba(
            "invalidni_vdovecky_sirotci_duchody", period
        )
        materska = osoba("materska", period)
        nemocenska = osoba("nemocenska", period)
        podpora_v_nezamestnanosti = osoba("podpora_v_nezamestnanosti", period)
        odmena_pestouna = osoba("odmena_pestouna", period)
        jine_prijmy = osoba("jine_prijmy", period)

        return (
            cisty_pracovni_prijem_osoby_bez_danoveho_bonusu
            + rodicovsky_prispevek
            + starobni_duchod
            + invalidni_vdovecky_sirotci_duchody
            + materska
            + nemocenska
            + podpora_v_nezamestnanosti
            + odmena_pestouna
            + jine_prijmy
        )
