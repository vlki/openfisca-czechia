from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_bonus_na_dite(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Bonus na dítě v rámci DSSP"

    def formula(domacnost, period, parameters):
        rozhodny_prijem = domacnost("dssp_rozhodny_prijem", period)
        zivotni_minimum = domacnost("zivotni_minimum_domacnosti", period)

        pocet_nezaopatrenych_deti = domacnost.sum(
            domacnost.members("je_nezaopatrene_dite", period)
        )
        castka_na_nezaopatrene_dite = domacnost(
            "dssp_castka_na_nezaopatrene_dite", period
        )

        zranitelne_osoby = domacnost.members("dssp_je_osoba_zranitelna", period)
        pracovne_aktivni_osoby = domacnost.members(
            "dssp_je_osoba_pracovne_aktivni", period
        )

        vsechny_osoby_zranitelne_nebo_pracovne_aktivni = domacnost.all(
            zranitelne_osoby | pracovne_aktivni_osoby
        )

        parametry_bonusu = parameters(period).dssp.bonus_na_dite

        hranice_rozhodneho_prijmu_pod_kterou_je_bonus_soucasti_davky = (
            parametry_bonusu.nasobek_zivotniho_minima_domacnosti_jako_hranice_rozhodneho_prijmu_pod_kterou_je_bonus_soucasti_davky
        ) * zivotni_minimum

        return where(
            (
                (
                    rozhodny_prijem
                    <= hranice_rozhodneho_prijmu_pod_kterou_je_bonus_soucasti_davky
                )
                and vsechny_osoby_zranitelne_nebo_pracovne_aktivni
            ),
            pocet_nezaopatrenych_deti * castka_na_nezaopatrene_dite,
            0,
        )
