from openfisca_core.model_api import select
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_soucet_castek_na_zivotni_potreby_clenu_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Součet částek na životní potřeby členů domácnosti"

    def formula(domacnost, period, parameters):
        zivotni_minimum = parameters(period).zivotni_minimum
        existencni_minimum = parameters(period).existencni_minimum

        #
        # Část 1: pro nezaopatřené děti bereme částky životního minima podle zákona o životním
        # a existenčním minumu (v zákoně 151/2025 Sb. § 36 odst. 2 písm. a))
        #

        vek_osob = domacnost.members("vek", period)
        jsou_osoby_nezaopatrene_deti = domacnost.members("je_nezaopatrene_dite", period)

        pocet_deti_do_6_let = domacnost.sum(
            jsou_osoby_nezaopatrene_deti & (vek_osob < 6)  # noqa: PLR2004
        )
        pocet_deti_6_az_15_let = domacnost.sum(
            jsou_osoby_nezaopatrene_deti & (vek_osob >= 6) & (vek_osob < 15)  # noqa: PLR2004
        )
        pocet_deti_15_az_26_let = domacnost.sum(
            jsou_osoby_nezaopatrene_deti & (vek_osob >= 15)  # noqa: PLR2004
        )

        castka_deti_do_6_let = (
            pocet_deti_do_6_let
            * zivotni_minimum.vice_osob_druha_nebo_dalsi_nezaopatrene_dite_do_6_let
        )
        castka_deti_6_az_15_let = (
            pocet_deti_6_az_15_let
            * zivotni_minimum.vice_osob_druha_nebo_dalsi_nezaopatrene_dite_6_az_15_let
        )
        castka_deti_15_az_26_let = (
            pocet_deti_15_az_26_let
            * zivotni_minimum.vice_osob_druha_nebo_dalsi_nezaopatrene_dite_15_az_26_let
        )

        #
        # Část 2: pro osoby, co nejsou nezaopatřené děti, ale jsou pracovně aktivní nebo zranitelné,
        # bereme částku existenčního minima podle zákona o životním a existenčním minumu (v zákoně
        # 151/2025 Sb. § 36 odst. 2 písm. b))
        #

        zranitelne_osoby = domacnost.members("dssp_je_osoba_zranitelna", period)
        pracovne_aktivni_osoby = domacnost.members(
            "dssp_je_osoba_pracovne_aktivni", period
        )

        pocet_nedeti = domacnost.sum(
            ~jsou_osoby_nezaopatrene_deti & (pracovne_aktivni_osoby | zranitelne_osoby)
        )
        castka_nedeti = pocet_nedeti * existencni_minimum

        #
        # Část 3: pro osoby z části 2, co plní podpůrný plán se jejich částka navyšuje o rozdíl mezi
        # částkou životního minima a částkou existenčního minima dle zákona o životním a existenčním
        # minimu (v zákoně 151/2025 Sb. § 36 odst. 3)
        #

        pocet_osob = domacnost.nb_persons()
        osoby_plnici_podpurny_plan = domacnost.members(
            "dssp_plni_osoba_podporny_plan", period
        )
        pocet_nedeti_plnici_podpurny_plan = domacnost.sum(
            ~jsou_osoby_nezaopatrene_deti
            & (pracovne_aktivni_osoby | zranitelne_osoby)
            & osoby_plnici_podpurny_plan
        )

        castka_navyseni_pro_nedeti = select(
            [
                pocet_nedeti_plnici_podpurny_plan == 0,
                pocet_osob == 1 and pocet_nedeti_plnici_podpurny_plan == 1,
                pocet_osob > 1,
            ],
            [
                # částka navýšení pro pocet_nedeti_plnici_podpurny_plan == 0
                0.0,
                # částka navyšení pro pocet_osob == 1 and pocet_nedeti_plnici_podpurny_plan == 1
                zivotni_minimum.jednotlivec - existencni_minimum,
                # částka navýšení pro pocet_osob > 1
                (
                    (zivotni_minimum.vice_osob_prvni - existencni_minimum)
                    + (
                        (pocet_nedeti_plnici_podpurny_plan - 1)
                        * (
                            zivotni_minimum.vice_osob_druha_nebo_dalsi_neni_nezaopatrene_dite
                            - existencni_minimum
                        )
                    )
                ),
            ],
            default=0.0,
        )

        return (
            castka_deti_do_6_let
            + castka_deti_6_az_15_let
            + castka_deti_15_az_26_let
            + castka_nedeti
            + castka_navyseni_pro_nedeti
        )
