from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.povinnost_odvodu_socialniho_pojisteni import (
    povinnost_odvodu_socialniho_pojisteni,
)


class povinnost_odvodu_socialniho_pojisteni_ze_zamestnani_2(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Povinnost odvodů sociálního pojištění z druhého zaměstnání"
    documentation = """
    Povinnost je navázaná na účast na nemocenském pojištění. U dohod se hranice pro povinnost
    odvodů testuje na úhrnu u téhož zaměstnavatele.

    Model oproti zákonu zjednodušuje: z pracovního poměru se odvádí vždy a do úhrnu
    pro dohody o pracovní činnosti se nezapočítává. Podrobnosti u sdílené funkce
    povinnost_odvodu_socialniho_pojisteni.
    """

    def formula(osoba, period, parameters):
        return povinnost_odvodu_socialniho_pojisteni(osoba, period, parameters, 2)
