from openfisca_core.model_api import max_, select, where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.stupen_invalidity import StupenInvalidity


class dpfo_z_hlavniho_zamestnani(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Daň z příjmu fyzických osob z hlavního zaměstnání"

    def formula(osoba, period, parameters):
        dpfo_pred_slevami = osoba(
            "dpfo_z_hlavniho_zamestnani_pred_uplatnenim_slev", period
        )
        danove_zvyhodneni_na_vyzivovane_deti = osoba(
            "danove_zvyhodneni_na_vyzivovane_deti_u_hlavniho_zamestnani", period
        )
        stupen_invalidity = osoba("stupen_invalidity", period)
        ma_prukaz_ztpp = osoba("ma_prukaz_ztpp", period)

        sleva_na_poplatnika = parameters(period).dpfo.sleva_na_poplatnika

        sleva_na_invaliditu = select(
            [
                stupen_invalidity == StupenInvalidity.stupen_1,
                stupen_invalidity == StupenInvalidity.stupen_2,
                stupen_invalidity == StupenInvalidity.stupen_3,
            ],
            [
                parameters(period).dpfo.sleva_na_invaliditu.stupen_1,
                parameters(period).dpfo.sleva_na_invaliditu.stupen_2,
                parameters(period).dpfo.sleva_na_invaliditu.stupen_3,
            ],
            default=0,
        )

        # Sleva na průkaz ZTP/P lze kombinovat se slevou na invaliditu
        sleva_na_prukaz_ztpp = where(
            ma_prukaz_ztpp, parameters(period).dpfo.sleva_na_prukaz_ztpp, 0
        )

        dpfo = max_(
            dpfo_pred_slevami
            - sleva_na_poplatnika
            - sleva_na_invaliditu
            - sleva_na_prukaz_ztpp,
            0,
        )

        # Daňové zvýhodnění může být vyšší než daň a pak se stává daňovým bonusem
        return dpfo - danove_zvyhodneni_na_vyzivovane_deti
