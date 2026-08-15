from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.stupen_invalidity import StupenInvalidity


class dssp_je_osoba_zranitelna_z_titulu_invalidity(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu invalidity v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        stupen_invalidity = osoba("stupen_invalidity", period)

        # § 7 odst. 1 c) Zranitelnou osobou je osoba invalidní ve druhém nebo třetím stupni
        return (stupen_invalidity == StupenInvalidity.stupen_2) | (
            stupen_invalidity == StupenInvalidity.stupen_3
        )
