import numpy as np

from openfisca_core.model_api import select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class danove_zvyhodneni_na_vyzivovane_deti_u_hlavniho_zamestnani(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daňové zvýhodnění na vyživované děti u hlavního zaměstnání"

    def formula(person, period, parameters):
        uplatnuje_danove_zvyhodneni = person(
            "uplatnuje_danove_zvyhodneni_na_vyzivovane_deti_u_hlavniho_zamestnani",
            period,
        )
        hruby_prijem = person("hruby_prijem_z_hlavniho_zamestnani", period)

        minimalni_mzda = parameters(period).minimalni_mzda

        # Polovina minimální mzdy ve výpočtu daňového zvýhodnění se zaokrouhluje
        # na celé koruny nahoru. Děláme nejdřív zaokrouhlení na 2 desetinná místa,
        # abychom odstranili artefakty po dělení Python float čísel.
        polovina_minimalni_mzdy = np.floor(np.round(minimalni_mzda / 2, decimals=2))

        je_nezaopatrene_dite = person("je_nezaopatrene_dite", period)
        ma_prukaz_ztpp = person("ma_prukaz_ztpp", period)
        vek_osoby = person("vek", period)

        pocet_deti_bez_ztpp = person.domacnost.sum(
            je_nezaopatrene_dite & (vek_osoby <= 26) & ~ma_prukaz_ztpp  # noqa: PLR2004
        )
        pocet_deti_se_ztpp = person.domacnost.sum(
            je_nezaopatrene_dite & (vek_osoby <= 26) & ma_prukaz_ztpp  # noqa: PLR2004
        )

        castky_zvyhodneni = parameters(period).dpfo.danove_zvyhodneni_na_vyzivovane_dite

        castka_za_prvni_bez_ztpp = where(
            pocet_deti_bez_ztpp > 0, castky_zvyhodneni.bez_ztpp_prvni_dite, 0
        )
        castka_za_druhe_bez_ztpp = where(
            pocet_deti_bez_ztpp > 1, castky_zvyhodneni.bez_ztpp_druhe_dite, 0
        )
        castka_za_treti_a_dalsi_bez_ztpp = where(
            pocet_deti_bez_ztpp > 2,  # noqa: PLR2004
            castky_zvyhodneni.bez_ztpp_treti_a_dalsi_dite * (pocet_deti_bez_ztpp - 2),
            0,
        )

        # Částky pro děti se ZTP/P by se měly započítávat až po částkách pro děti bez ZTP/P,
        # aby tak byla maximalizovaná celková částka zvýhodnění pro rodinu (částky pro ZTP/P
        # jsou totiž vyšší než ty pro děti bez)
        castka_za_prvni_se_ztpp = where(
            (pocet_deti_se_ztpp > 0) & (pocet_deti_bez_ztpp == 0),
            castky_zvyhodneni.se_ztpp_prvni_dite,
            0,
        )
        castka_za_druhe_se_ztpp = where(
            (
                ((pocet_deti_se_ztpp > 1) & (pocet_deti_bez_ztpp == 0))
                | ((pocet_deti_se_ztpp > 0) & (pocet_deti_bez_ztpp == 1))
            ),
            castky_zvyhodneni.se_ztpp_druhe_dite,
            0,
        )
        pocet_deti_treti_a_dalsi_se_ztpp = select(
            [
                (pocet_deti_se_ztpp > 2) & (pocet_deti_bez_ztpp == 0),  # noqa: PLR2004
                (pocet_deti_se_ztpp > 1) & (pocet_deti_bez_ztpp == 1),
                (pocet_deti_se_ztpp > 0) & (pocet_deti_bez_ztpp == 2),  # noqa: PLR2004
            ],
            [pocet_deti_se_ztpp - 2, pocet_deti_se_ztpp - 1, pocet_deti_se_ztpp],
            default=0,
        )
        castka_za_treti_a_dalsi_se_ztpp = where(
            pocet_deti_treti_a_dalsi_se_ztpp > 0,
            castky_zvyhodneni.se_ztpp_treti_a_dalsi_dite
            * pocet_deti_treti_a_dalsi_se_ztpp,
            0,
        )

        soucet_castek_zvyhodneni = (
            castka_za_prvni_bez_ztpp
            + castka_za_druhe_bez_ztpp
            + castka_za_treti_a_dalsi_bez_ztpp
            + castka_za_prvni_se_ztpp
            + castka_za_druhe_se_ztpp
            + castka_za_treti_a_dalsi_se_ztpp
        )

        return where(
            # Daňové zvýhodnění lze uplatnit pouze při mzdě ve výši aspoň poloviny
            # minimální mzdy
            uplatnuje_danove_zvyhodneni & (hruby_prijem >= polovina_minimalni_mzdy),
            soucet_castek_zvyhodneni,
            0,
        )
