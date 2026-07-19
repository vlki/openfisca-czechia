from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_vlastnicky_pausal_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Vlastnický paušál domácnosti v rámci DSSP"

    def formula(domacnost, period, parameters):
        normativni_najemne = domacnost("dssp_normativni_najemne_domacnosti", period)
        naklady_spojene_s_uzivanim_bytu = domacnost(
            "dssp_naklady_spojene_s_uzivanim_bytu", period
        )

        parametry_pausalu = parameters(
            period
        ).dssp.slozka_na_bydleni.vlastnicky_pausal_domacnosti

        cast_pismeno_a = (
            parametry_pausalu.podil_normativniho_najemneho_ve_vypoctu_vlastnickeho_pausalu
            * (normativni_najemne - naklady_spojene_s_uzivanim_bytu),
        )

        cast_pismeno_b = naklady_spojene_s_uzivanim_bytu

        return cast_pismeno_a + cast_pismeno_b
