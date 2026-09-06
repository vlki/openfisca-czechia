from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class cisty_pracovni_prijem_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Čistý pracovní příjem osoby"

    def formula(osoba, period, parameters):
        hruby_pracovni_prijem = osoba("hruby_pracovni_prijem_osoby", period)
        srazkova_dan = osoba("srazkova_dan_z_prijmu_osoby", period)
        # Záloha může být záporná, pokud daňové zvýhodnění na vyživované děti
        # přesáhne daň. V takovém případě se čistý příjem o daňový bonus zvyšuje.
        zaloha_na_dan = osoba("zaloha_na_dan_z_prijmu_osoby", period)
        odvod_socialniho_pojisteni = osoba("odvod_socialniho_pojisteni_osoby", period)
        odvod_zdravotniho_pojisteni = osoba("odvod_zdravotniho_pojisteni_osoby", period)

        return (
            hruby_pracovni_prijem
            - srazkova_dan
            - zaloha_na_dan
            - odvod_socialniho_pojisteni
            - odvod_zdravotniho_pojisteni
        )
