from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class plati_stat_zdravotni_pojisteni(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda stát platí za osobu zdravotní pojištění"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        je_nezaopatrene_dite = osoba("je_nezaopatrene_dite", period)
        starobni_duchod = osoba("starobni_duchod", period)
        invalidni_vdovecky_sirotci_duchody = osoba(
            "invalidni_vdovecky_sirotci_duchody", period
        )
        materska = osoba("materska", period)
        rodicovsky_prispevek = osoba("rodicovsky_prispevek", period)

        return (
            je_nezaopatrene_dite
            | (starobni_duchod > 0)
            | (invalidni_vdovecky_sirotci_duchody > 0)
            | (materska > 0)
            | (rodicovsky_prispevek > 0)
        )
