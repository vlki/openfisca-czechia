from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class zakladni_nezabavitelna_castka_na_osobu_vyzivovanou_v_exekuci_nebo_insolvenci(
    Variable
):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Základní nezabavitelná částka na osobu povinného pro výpočet srážky v exekuci nebo insolvenci"

    def formula(osoba, period, parameters):
        zakladni_nezabavitelna_castka_na_osobu_povinneho = osoba(
            "zakladni_nezabavitelna_castka_na_osobu_povinneho_v_exekuci_nebo_insolvenci",
            period,
        )
        podil_ve_vypoctu_castky_osoby_vyzivovane = parameters(
            period
        ).exekuce_a_insolvence.zakladni_nezabavitelna_castka.podil_ve_vypoctu_castky_osoby_vyzivovane

        return (
            podil_ve_vypoctu_castky_osoby_vyzivovane
            * zakladni_nezabavitelna_castka_na_osobu_povinneho
        )
