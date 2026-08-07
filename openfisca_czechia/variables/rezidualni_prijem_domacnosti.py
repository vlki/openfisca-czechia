from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class rezidualni_prijem_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Reziduální příjem domácnosti"

    def formula(domacnost, period, parameters):
        cisty_penezni_prijem_domacnosti_po_srazkach = domacnost(
            "cisty_penezni_prijem_domacnosti_po_srazkach", period
        )
        celkove_naklady_na_bydleni = domacnost("celkove_naklady_na_bydleni", period)
        celkove_pojistne_samoplatcu_zdravotniho_pojisteni_v_domacnosti = domacnost(
            "celkove_pojistne_samoplatcu_zdravotniho_pojisteni_v_domacnosti", period
        )

        return (
            cisty_penezni_prijem_domacnosti_po_srazkach
            - celkove_naklady_na_bydleni
            - celkove_pojistne_samoplatcu_zdravotniho_pojisteni_v_domacnosti
        )
