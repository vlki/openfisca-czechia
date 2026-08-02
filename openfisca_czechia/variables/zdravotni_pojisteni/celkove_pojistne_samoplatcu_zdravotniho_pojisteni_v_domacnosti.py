from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class celkove_pojistne_samoplatcu_zdravotniho_pojisteni_v_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Celkové pojistné placené samoplátci zdravotního pojištění v domácnosti"

    def formula(domacnost, period, parameters):
        samoplatci_zdravotniho_pojisteni = domacnost.members(
            "je_samoplatce_zdravotniho_pojisteni", period
        )
        vyse_pojistneho_pro_samoplatce_zdravotniho_pojisteni = domacnost.members(
            "vyse_pojistneho_pro_samoplatce_zdravotniho_pojisteni", period
        )

        pojistne_jen_samoplatcu = where(
            samoplatci_zdravotniho_pojisteni,
            vyse_pojistneho_pro_samoplatce_zdravotniho_pojisteni,
            0,
        )

        return domacnost.sum(pojistne_jen_samoplatcu)
