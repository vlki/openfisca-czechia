from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.je_prvni_zamestnani_u_daneho_zamestnavatele import (
    je_prvni_zamestnani_u_daneho_zamestnavatele,
)


class je_zamestnani_3_prvni_u_daneho_zamestnavatele(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Zda je třetí zaměstnání první u daného zaměstnavatele"
    documentation = """
    Zálohu na daň počítá zaměstnavatel jednou z úhrnu příjmů. Aby se při více
    zaměstnáních u téhož zaměstnavatele nezapočítala vícekrát, přiřazuje se
    zaměstnání s nejnižším indexem.
    """

    def formula(osoba, period, parameters):
        return je_prvni_zamestnani_u_daneho_zamestnavatele(osoba, period, 3)
