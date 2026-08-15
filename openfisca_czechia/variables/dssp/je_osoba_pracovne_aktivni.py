from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_pracovne_aktivni(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba pracovně aktivní v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        cisty_pracovni_prijem_osoby = osoba("cisty_pracovni_prijem_osoby", period)
        nemocenska = osoba("nemocenska", period)
        je_registrovana_na_uradu_prace = osoba("je_registrovana_na_uradu_prace", period)
        odmena_pestouna = osoba("odmena_pestouna", period)
        prispevek_na_uhradu_potreb_na_dite = osoba(
            "prispevek_na_uhradu_potreb_na_dite", period
        )
        ma_sverene_dite_do_pece_max_2_roky = osoba(
            "ma_sverene_dite_do_pece_max_2_roky", period
        )

        return (
            (cisty_pracovni_prijem_osoby != 0)
            | (nemocenska > 0)
            | je_registrovana_na_uradu_prace
            | (odmena_pestouna > 0)
            | (
                (prispevek_na_uhradu_potreb_na_dite > 0)
                & ma_sverene_dite_do_pece_max_2_roky
            )
        )
