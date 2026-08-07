from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class castka_nad_kterou_se_v_exekuci_a_insolvenci_srazi_bez_omezeni(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Částka, nad kterou se v exekuci a insolvenci sráží bez omezení"

    def formula(osoba, period, parameters):
        zm_jednotlivce = parameters(period).zivotni_minimum.jednotlivec
        normativni_najemne = parameters(
            period
        ).dssp.slozka_na_bydleni.normativni_najemne.jednoclenna_domacnost.obec_70000_obyvatel_a_vice
        energeticky_pausal = parameters(
            period
        ).dssp.slozka_na_bydleni.energeticky_pausal.jednoclenna_domacnost
        nasobek_ve_vypoctu_castky = parameters(
            period
        ).exekuce_a_insolvence.castka_nad_kterou_se_srazi_bez_omezeni

        return nasobek_ve_vypoctu_castky * (
            zm_jednotlivce + normativni_najemne + energeticky_pausal
        )
