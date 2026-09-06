from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.typ_pracovni_smlouvy import (
    TypPracovniSmlouvy,
)
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.uhrn_prijmu_z_typu_smlouvy_u_stejneho_zamestnavatele import (
    uhrn_prijmu_z_typu_smlouvy_u_stejneho_zamestnavatele,
)


class uhrn_prijmu_z_dpc_u_stejneho_zamestnavatele_zamestnani_1(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = (
        "Úhrn příjmů z dohod o pracovní činnosti u zaměstnavatele prvního zaměstnání"
    )
    documentation = """
    Úhrn hrubých příjmů ze všech zaměstnání na dohodu o pracovní činnosti, která jsou
    u téhož zaměstnavatele jako prvního zaměstnání. Na tomto úhrnu se testuje
    hranice pro povinnost odvodů i hranice pro srážkovou daň.

    Příjem z pracovního poměru se sem nezapočítává, viz zjednodušení popsané
    u proměnné podleha_prijem_ze_zamestnani_1_srazkove_dani.
    """

    def formula(osoba, period, parameters):
        return uhrn_prijmu_z_typu_smlouvy_u_stejneho_zamestnavatele(
            osoba, period, 1, TypPracovniSmlouvy.dpc
        )
