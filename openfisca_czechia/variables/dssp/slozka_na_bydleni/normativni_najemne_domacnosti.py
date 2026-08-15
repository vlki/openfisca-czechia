import numpy as np

from openfisca_core.model_api import select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost
from openfisca_czechia.variables.dssp.slozka_na_bydleni.okres_bydliste import (
    DsspOkresBydliste,
)


class dssp_normativni_najemne_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Normativní nájemné domácnosti v rámci DSSP"

    def formula(domacnost, period, parameters):
        """
        Výpočet normativního nájemného domácnosti podle velikosti domácnosti (před říjnem 2026)
        """

        pocet_osob = domacnost(
            "dssp_pocet_osob_v_domacnosti_pro_vypocet_nakladu_na_bydleni", period
        )
        velikost_obce_bydliste = domacnost("dssp_velikost_obce_bydliste", period)
        vsechny_osoby_zranitelne = domacnost(
            "dssp_jsou_vsechny_osoby_v_domacnosti_zranitelne", period
        )

        klic_velikosti_domacnosti = select(
            [
                pocet_osob <= 1,
                pocet_osob == 2,  # noqa: PLR2004
                pocet_osob == 3,  # noqa: PLR2004
                pocet_osob == 4,  # noqa: PLR2004
                pocet_osob >= 5,  # noqa: PLR2004
            ],
            [
                "jednoclenna_domacnost",
                "dvouclenna_domacnost",
                "triclenna_domacnost",
                "ctyrclenna_domacnost",
                "peti_nebo_viceclenna_domacnost",
            ],
            default="",
        )

        normativni_najemne_pro_zranitelne = parameters(
            period
        ).dssp.slozka_na_bydleni.normativni_najemne_dle_velikosti_obce.pro_zranitelne[
            klic_velikosti_domacnosti
        ][velikost_obce_bydliste]
        normativni_najemne_pro_nezranitelne = parameters(
            period
        ).dssp.slozka_na_bydleni.normativni_najemne_dle_velikosti_obce.pro_nezranitelne[
            klic_velikosti_domacnosti
        ][velikost_obce_bydliste]

        return where(
            vsechny_osoby_zranitelne,
            normativni_najemne_pro_zranitelne,
            normativni_najemne_pro_nezranitelne,
        )

    def formula_2026_10_01(domacnost, period, parameters):
        """
        Výpočet normativního nájemného domácnosti podle okresu (od října 2026)
        """

        pocet_osob = domacnost(
            "dssp_pocet_osob_v_domacnosti_pro_vypocet_nakladu_na_bydleni", period
        )
        okres_bydliste = domacnost("dssp_okres_bydliste", period)
        vsechny_osoby_zranitelne = domacnost(
            "dssp_jsou_vsechny_osoby_v_domacnosti_zranitelne", period
        )

        normativy_z_parametru = parameters(
            period
        ).dssp.slozka_na_bydleni.normativni_najemne_dle_okresu

        # Normativy v parametrech jsou ve složkách podle krajů, pro vyhledání podle okresu je zploštíme
        normativy_z_parametru_bez_kraju = {
            okres: normativy_z_parametru[kraj][okres]
            for kraj in normativy_z_parametru
            for okres in normativy_z_parametru[kraj]
        }

        klice_velikosti_domacnosti = (
            "jednoclenna_domacnost",
            "dvouclenna_domacnost",
            "triclenna_domacnost",
            "ctyrclenna_domacnost",
            "peti_nebo_viceclenna_domacnost",
        )

        # Vytvoří tříúrovňové pole hodnot tak, aby šlo vybrat normativní nájemné tím, že
        # se zadá index okresu (pořadí dle v DsspOkresBydliste, tj. praha = 0, blansko = 1,
        # atd.), index velikosti domácnosti (1členná = 0, 2členná = 1, atd.) a index
        # zranitelnosti (nezranitelná = 0, zranitelná = 1).
        normativy_dle_okresu_velikosti_a_zranitelnosti = np.array(
            [
                [
                    [
                        normativy_z_parametru_bez_kraju[okres.name][
                            klic_velikosti_domacnosti
                        ].nezranitelna,
                        normativy_z_parametru_bez_kraju[okres.name][
                            klic_velikosti_domacnosti
                        ].zranitelna,
                    ]
                    for klic_velikosti_domacnosti in klice_velikosti_domacnosti
                ]
                for okres in DsspOkresBydliste
            ]
        )

        # Pro 1člennou domácnosti bude index 0
        # Pro 2člennou domácnosti bude index 1
        # Pro 3člennou domácnosti bude index 2
        # Pro 4člennou domácnosti bude index 3
        # Pro 5-a-více-člennou domácnosti bude index 4
        index_velikosti = np.clip(pocet_osob, 1, len(klice_velikosti_domacnosti)) - 1

        # astype(int) převede na číslo tak, že nezranitelná domácnost je 0 a zranitelná 1
        index_zranitelnosti = vsechny_osoby_zranitelne.astype(int)

        return normativy_dle_okresu_velikosti_a_zranitelnosti[
            # Okres takto zadaný se použije jako číselný index
            okres_bydliste,
            index_velikosti,
            index_zranitelnosti,
        ]
