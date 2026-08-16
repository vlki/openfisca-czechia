import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_pecujiciho_rodice(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu pečujícího rodiče v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        je_rodic_pecujici_o_dite = osoba("je_rodic_pecujici_o_dite", period)

        pocet_rodicu_v_domacnosti = osoba.domacnost.sum(osoba("je_rodic", period))
        je_osamely_rodic = pocet_rodicu_v_domacnosti == 1

        vek_osob_v_domacnosti = osoba.domacnost.members("vek", period)
        vek_nejmladsiho_ditete_v_domacnosti = osoba.domacnost.min(
            where(
                osoba("je_nezaopatrene_dite", period),
                vek_osob_v_domacnosti,
                np.iinfo(np.int32).max,
            )
        )

        parametry = parameters(
            period
        ).dssp.zranitelna_osoba.zranitelna_osoba_z_titulu_pecujiciho_rodice

        vekova_hranice_ditete = where(
            je_osamely_rodic,
            parametry.pecujici_osamely_rodic_je_zranitelny_do_maximalniho_veku_ditete,
            parametry.pecujici_rodic_je_zranitelny_do_maximalniho_veku_ditete,
        )

        return je_rodic_pecujici_o_dite & (
            vek_nejmladsiho_ditete_v_domacnosti <= vekova_hranice_ditete
        )
