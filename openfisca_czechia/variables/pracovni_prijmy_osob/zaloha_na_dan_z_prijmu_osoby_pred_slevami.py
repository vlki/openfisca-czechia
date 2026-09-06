from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class zaloha_na_dan_z_prijmu_osoby_pred_slevami(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = (
        "Celková záloha na daň z příjmu osoby ze všech zaměstnání před uplatněním slev"
    )
    documentation = """
    Součet záloh, které jednotliví zaměstnavatelé spočítají ze svých základů, ještě před
    uplatněním měsíčních slev na dani podle § 35ba a měsíčního daňového zvýhodnění na
    vyživované děti. Slevy se uplatní jen ze zálohy u zaměstnavatele s podepsaným
    prohlášením, výsledek po nich je v zaloha_na_dan_z_prijmu_osoby.
    """

    def formula(osoba, period, parameters):
        zaloha = 0.0
        for index in INDEXY_ZAMESTNANI:
            zaloha = zaloha + osoba(
                f"zaloha_na_dan_pred_slevami_ze_zamestnani_{index}", period
            )

        return zaloha
