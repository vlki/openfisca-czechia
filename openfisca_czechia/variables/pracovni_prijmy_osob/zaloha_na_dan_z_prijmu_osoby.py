from openfisca_core.model_api import max_, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class zaloha_na_dan_z_prijmu_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Celková záloha na daň z příjmu osoby ze všech zaměstnání"
    documentation = """
    Zálohy jednotlivých zaměstnavatelů po uplatnění slev. Slevy podle § 35ba se
    uplatní jen ze zálohy u zaměstnavatele, u kterého je podepsané prohlášení
    k dani, a nejvýše do nuly. Do daňového bonusu může jít pouze daňové zvýhodnění
    na vyživované děti, proto může být výsledek záporný.
    """

    def formula(osoba, period, parameters):
        zaloha_celkem = 0.0
        zaloha_u_zamestnavatele_s_prohlasenim = 0.0

        for index in INDEXY_ZAMESTNANI:
            zaloha_ze_zamestnani = osoba(
                f"zaloha_na_dan_pred_slevami_ze_zamestnani_{index}", period
            )
            je_podepsane_prohlaseni = osoba(
                f"je_podepsane_prohlaseni_k_dani_u_zamestnani_{index}", period
            )

            zaloha_celkem = zaloha_celkem + zaloha_ze_zamestnani
            zaloha_u_zamestnavatele_s_prohlasenim = (
                zaloha_u_zamestnavatele_s_prohlasenim
                + where(je_podepsane_prohlaseni, zaloha_ze_zamestnani, 0)
            )

        zaloha_u_ostatnich_zamestnavatelu = (
            zaloha_celkem - zaloha_u_zamestnavatele_s_prohlasenim
        )

        sleva_na_poplatnika = osoba("sleva_na_poplatnika", period)
        sleva_na_invaliditu = osoba("sleva_na_invaliditu", period)
        sleva_na_prukaz_ztpp = osoba("sleva_na_prukaz_ztpp", period)
        danove_zvyhodneni_na_vyzivovane_deti = osoba(
            "danove_zvyhodneni_na_vyzivovane_deti", period
        )

        zaloha_po_slevach = max_(
            zaloha_u_zamestnavatele_s_prohlasenim
            - sleva_na_poplatnika
            - sleva_na_invaliditu
            - sleva_na_prukaz_ztpp,
            0,
        )

        zaloha = (
            zaloha_u_ostatnich_zamestnavatelu
            + zaloha_po_slevach
            - danove_zvyhodneni_na_vyzivovane_deti
        )

        # Měsíční daňový bonus se podle § 35d odst. 4 vyplatí, jen činí-li aspoň
        # 50 Kč. Pod touto hranicí se záloha nesnižuje pod nulu.
        minimalni_mesicni_danovy_bonus = parameters(
            period
        ).dpfo.minimalni_mesicni_danovy_bonus

        zaloha = where(
            -zaloha < minimalni_mesicni_danovy_bonus, max_(zaloha, 0), zaloha
        )

        return zaloha
