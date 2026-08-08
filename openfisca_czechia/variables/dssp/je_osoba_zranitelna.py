from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.stupen_invalidity import StupenInvalidity


class dssp_je_osoba_zranitelna(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná v rámci DSSP"
    definition_period = MONTH

    def formula(osoba, period, parameters):
        je_nezaopatrene_dite = osoba("je_nezaopatrene_dite", period)
        starobni_duchod = osoba("starobni_duchod", period)
        stupen_invalidity = osoba("stupen_invalidity", period)
        materska = osoba("materska", period)

        return (
            je_nezaopatrene_dite
            | (starobni_duchod > 0)
            | (stupen_invalidity == StupenInvalidity.stupen_2)
            | (stupen_invalidity == StupenInvalidity.stupen_3)
            | (materska > 0)
        )
