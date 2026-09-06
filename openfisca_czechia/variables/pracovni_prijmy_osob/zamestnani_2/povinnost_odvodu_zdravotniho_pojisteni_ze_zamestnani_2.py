from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.povinnost_odvodu_zdravotniho_pojisteni import (
    povinnost_odvodu_zdravotniho_pojisteni,
)


class povinnost_odvodu_zdravotniho_pojisteni_ze_zamestnani_2(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Povinnost odvodů zdravotního pojištění z druhého zaměstnání"
    documentation = """
    Kdo je zaměstnancem pro účely veřejného zdravotního pojištění, určuje
    § 5 písm. a) zákona č. 48/1997 Sb. U dohod se hranice pro povinnost
    odvodů testuje na úhrnu u téhož zaměstnavatele.

    Model oproti zákonu zjednodušuje: z pracovního poměru se odvádí vždy a do úhrnu
    pro dohody o pracovní činnosti se nezapočítává. Podrobnosti u sdílené funkce
    povinnost_odvodu_zdravotniho_pojisteni.
    """

    def formula(osoba, period, parameters):
        return povinnost_odvodu_zdravotniho_pojisteni(osoba, period, parameters, 2)
