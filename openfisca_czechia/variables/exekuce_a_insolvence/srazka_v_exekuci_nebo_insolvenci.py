import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class srazka_v_exekuci_nebo_insolvenci(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Srážka z příjmu osoby v exekuci nebo insolvenci"

    def formula(osoba, period, parameters):
        pocet_exekuci_osoby = osoba("pocet_exekuci_osoby", period)
        ma_prednostni_exekuce = osoba("ma_prednostni_exekuce", period)
        je_v_insolvenci = osoba("je_v_insolvenci", period)

        zbytek_po_odecteni_nezabavitelne_castky = osoba(
            "zbytek_z_prijmu_osoby_po_odecteni_nezabavitelne_castky_v_exekuci_nebo_insolvenci",
            period,
        )
        castka_nad_kterou_se_srazi_bez_omezeni = osoba(
            "castka_nad_kterou_se_v_exekuci_a_insolvenci_srazi_bez_omezeni", period
        )

        castka_srazena_castecne = where(
            (
                zbytek_po_odecteni_nezabavitelne_castky
                > castka_nad_kterou_se_srazi_bez_omezeni
            ),
            castka_nad_kterou_se_srazi_bez_omezeni,
            zbytek_po_odecteni_nezabavitelne_castky,
        )
        castka_srazena_bez_omezeni = where(
            (
                zbytek_po_odecteni_nezabavitelne_castky
                > castka_nad_kterou_se_srazi_bez_omezeni
            ),
            (
                zbytek_po_odecteni_nezabavitelne_castky
                - castka_nad_kterou_se_srazi_bez_omezeni
            ),
            0,
        )

        # Zaokrouhluje se na koruny dolů. Nejdřív děláme round na 2 desetinná
        # místa, aby se odstranily artefakty po dělení Python float čísel
        tretina_z_castky_srazene_castecne = np.floor(
            np.round(castka_srazena_castecne / 3, decimals=2)
        )

        # TODO: Dát číslo 4 do parametrů
        pocet_zabavenych_tretin = where(
            (
                ((pocet_exekuci_osoby > 0) & ma_prednostni_exekuce)
                | (pocet_exekuci_osoby >= 4)  # noqa: PLR2004
                | je_v_insolvenci
            ),
            2,
            1,
        )

        srazka = (
            pocet_zabavenych_tretin * tretina_z_castky_srazene_castecne
            + castka_srazena_bez_omezeni
        )

        return where((pocet_exekuci_osoby > 0) | je_v_insolvenci, srazka, 0)
