from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class zivotni_minimum_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Životní minimum domácnosti"

    def formula(domacnost, period, parameters):
        pocet_osob = domacnost.nb_persons()
        vek_osob = domacnost.members("vek", period)
        jsou_osoby_nezaopatrene_deti = domacnost.members("je_nezaopatrene_dite", period)

        pocet_nedeti = domacnost.sum(~jsou_osoby_nezaopatrene_deti)
        pocet_deti_do_6_let = domacnost.sum(
            jsou_osoby_nezaopatrene_deti & (vek_osob < 6)  # noqa: PLR2004
        )
        pocet_deti_6_az_15_let = domacnost.sum(
            jsou_osoby_nezaopatrene_deti & (vek_osob >= 6) & (vek_osob < 15)  # noqa: PLR2004
        )
        pocet_deti_15_az_26_let = domacnost.sum(
            jsou_osoby_nezaopatrene_deti & (vek_osob >= 15)  # noqa: PLR2004
        )

        zivotni_minimum = parameters(period).zivotni_minimum

        castka_nedeti = where(
            pocet_nedeti >= 1,
            zivotni_minimum.vice_osob_prvni
            + (
                (pocet_nedeti - 1)
                * zivotni_minimum.vice_osob_druha_nebo_dalsi_neni_nezaopatrene_dite
            ),
            0,
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

        return where(
            pocet_osob == 1,
            zivotni_minimum.jednotlivec,
            (
                castka_nedeti
                + castka_deti_do_6_let
                + castka_deti_6_az_15_let
                + castka_deti_15_az_26_let
            ),
        )
