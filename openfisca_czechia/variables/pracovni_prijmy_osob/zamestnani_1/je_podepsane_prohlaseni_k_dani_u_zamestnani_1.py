from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.je_u_zamestnani_podepsane_prohlaseni_k_dani import (
    je_u_zamestnani_podepsane_prohlaseni_k_dani,
)


class je_podepsane_prohlaseni_k_dani_u_zamestnani_1(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Zda je u prvního zaměstnání podepsané prohlášení k dani"

    def formula(osoba, period, parameters):
        return je_u_zamestnani_podepsane_prohlaseni_k_dani(osoba, period, 1)
