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

        cast_pismeno_a = (
            # TODO: move to parameter
            0.3 * (normativni_najemne - naklady_spojene_s_uzivanim_bytu)
        )

        cast_pismeno_b = naklady_spojene_s_uzivanim_bytu

        return cast_pismeno_a + cast_pismeno_b
