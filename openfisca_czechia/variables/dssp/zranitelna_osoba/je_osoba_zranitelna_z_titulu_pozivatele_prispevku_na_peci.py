from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.nepracovni_prijmy_osob.stupen_zavislosti_prispevku_na_peci import (
    StupenZavislostiPrispevkuNaPeci,
)


class dssp_je_osoba_zranitelna_z_titulu_pozivatele_prispevku_na_peci(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu poživatele příspěvku na péči v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        prispevek_na_peci = osoba("prispevek_na_peci", period)
        stupen_zavislosti = osoba("stupen_zavislosti_prispevku_na_peci", period)

        # § 7 odst. 1 g) Zranitelnou osobou je poživatel příspěvku na péči ve stupni II nebo vyšším
        return (prispevek_na_peci > 0) & (
            (stupen_zavislosti == StupenZavislostiPrispevkuNaPeci.stupen_2)
            | (stupen_zavislosti == StupenZavislostiPrispevkuNaPeci.stupen_3)
            | (stupen_zavislosti == StupenZavislostiPrispevkuNaPeci.stupen_4)
        )
