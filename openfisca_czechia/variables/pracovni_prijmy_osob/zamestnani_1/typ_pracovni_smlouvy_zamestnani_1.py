from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.typ_pracovni_smlouvy import (
    TypPracovniSmlouvy,
)


class typ_pracovni_smlouvy_zamestnani_1(Variable):
    value_type = Enum
    possible_values = TypPracovniSmlouvy
    default_value = TypPracovniSmlouvy.hpp
    entity = Osoba
    definition_period = MONTH
    label = "Typ pracovní smlouvy prvního zaměstnání"
