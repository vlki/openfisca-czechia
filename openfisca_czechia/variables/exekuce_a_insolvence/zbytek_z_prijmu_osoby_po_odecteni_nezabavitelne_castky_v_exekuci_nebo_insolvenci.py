from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class zbytek_z_prijmu_osoby_po_odecteni_nezabavitelne_castky_v_exekuci_nebo_insolvenci(
    Variable
):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Zbytek z příjmu osoby pro odečtení nezabavitelné částky v exekuci nebo insolvenci"

    def formula(osoba, period, parameters):
        prijem_osoby = osoba(
            "prijem_osoby_pro_vypocet_srazky_v_exekuci_nebo_insolvenci",
            period,
        )
        zakladni_nezabavitelna_castka = osoba(
            "zakladni_nezabavitelna_castka_osoby_v_exekuci_nebo_insolvenci",
            period,
        )

        return prijem_osoby - zakladni_nezabavitelna_castka
