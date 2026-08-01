from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost
from openfisca_czechia.variables.bydleni.vztah_k_nemovitosti import VztahKNemovitosti


class celkove_naklady_na_bydleni(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Celkové náklady domácnosti na bydlení"

    def formula(domacnost, period, parameters):
        vztah_k_nemovitosti = domacnost("vztah_k_nemovitosti", period)

        naklady_na_najemne = domacnost("naklady_na_najemne", period)
        dalsi_poplatky_spojene_s_bydlenim = domacnost(
            "dalsi_poplatky_spojene_s_bydlenim", period
        )
        naklady_na_energie = domacnost("naklady_na_energie", period)

        zapocitane_najemne = where(
            vztah_k_nemovitosti == VztahKNemovitosti.najemni_podnajemni,
            naklady_na_najemne,
            0,
        )

        return (
            zapocitane_najemne + dalsi_poplatky_spojene_s_bydlenim + naklady_na_energie
        )
