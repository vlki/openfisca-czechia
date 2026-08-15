from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_prijemce_starobniho_duchodu(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu příjemce starobního důchodu v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        starobni_duchod = osoba("starobni_duchod", period)

        # § 7 odst. 1 b) Zranitelnou osobou je poživatel starobního důchodu
        return starobni_duchod > 0
