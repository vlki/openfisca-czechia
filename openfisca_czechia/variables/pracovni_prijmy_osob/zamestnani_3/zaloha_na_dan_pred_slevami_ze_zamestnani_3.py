from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.zaloha_pred_slevami import (
    zaloha_pred_slevami,
)


class zaloha_na_dan_pred_slevami_ze_zamestnani_3(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Záloha na daň u zaměstnavatele třetího zaměstnání před uplatněním slev"
    documentation = """
    Zálohu počítá každý plátce daně samostatně, včetně vlastní hranice pro vyšší
    sazbu daně. Souběh u více zaměstnavatelů se vyrovnává až v ročním zúčtování
    nebo v daňovém přiznání, které tento model nepokrývá.
    """

    def formula(osoba, period, parameters):
        zaklad_dane = osoba(
            "zaklad_dane_pro_zalohu_u_zamestnavatele_zamestnani_3", period
        )

        return zaloha_pred_slevami(zaklad_dane, period, parameters)
