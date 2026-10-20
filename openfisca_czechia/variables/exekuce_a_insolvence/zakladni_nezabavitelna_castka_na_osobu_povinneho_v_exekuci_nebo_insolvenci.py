from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class zakladni_nezabavitelna_castka_na_osobu_povinneho_v_exekuci_nebo_insolvenci(
    Variable
):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Základní nezabavitelná částka na osobu povinného pro výpočet srážky v exekuci nebo insolvenci"

    def formula(osoba, period, parameters):
        # § 4 nařízení vlády č. 595/2006 Sb.: částky životního minima, normativního
        # nájemného a energetického paušálu se berou ve výši k 1. lednu roku,
        # do kterého spadá výplata mzdy. Změny během roku se tak neprojeví.
        k_1_lednu = period.start.offset("first-of", "year")

        zm_jednotlivce = parameters(k_1_lednu).zivotni_minimum.jednotlivec
        normativni_najemne = parameters(
            k_1_lednu
        ).dssp.slozka_na_bydleni.normativni_najemne_dle_velikosti_obce.pro_nezranitelne.jednoclenna_domacnost.obec_70000_obyvatel_a_vice
        energeticky_pausal = parameters(
            k_1_lednu
        ).dssp.slozka_na_bydleni.energeticky_pausal.jednoclenna_domacnost
        podil_ve_vypoctu_castky_osoby_povinneho = parameters(
            period
        ).exekuce_a_insolvence.zakladni_nezabavitelna_castka.podil_ve_vypoctu_castky_osoby_povinneho

        return podil_ve_vypoctu_castky_osoby_povinneho * (
            zm_jednotlivce + normativni_najemne + energeticky_pausal
        )
