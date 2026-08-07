import numpy as np

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class zakladni_nezabavitelna_castka_osoby_v_exekuci_nebo_insolvenci(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Základní nezabavitelná částka osoby pro výpočet srážky v exekuci nebo insolvenci"

    def formula(osoba, period, parameters):
        zakladni_nezabavitelna_castka_na_osobu_povinneho = osoba(
            "zakladni_nezabavitelna_castka_na_osobu_povinneho_v_exekuci_nebo_insolvenci",
            period,
        )
        zakladni_nezabavitelna_castka_na_osobu_vyzivovanou = osoba(
            "zakladni_nezabavitelna_castka_na_osobu_vyzivovanou_v_exekuci_nebo_insolvenci",
            period,
        )
        pocet_vyzivovanych_osob = osoba(
            "pocet_vyzivovanych_osob_pro_vypocet_srazky_v_exekuci_nebo_insolvenci",
            period,
        )

        return np.round(
            zakladni_nezabavitelna_castka_na_osobu_povinneho
            + (
                pocet_vyzivovanych_osob
                * zakladni_nezabavitelna_castka_na_osobu_vyzivovanou
            )
        )
