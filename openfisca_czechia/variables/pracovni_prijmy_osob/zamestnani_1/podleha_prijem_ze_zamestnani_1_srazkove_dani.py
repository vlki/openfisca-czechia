from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.podleha_prijem_srazkove_dani import (
    podleha_prijem_srazkove_dani,
)


class podleha_prijem_ze_zamestnani_1_srazkove_dani(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Zda příjem z prvního zaměstnání podléhá srážkové dani"
    documentation = """
    Podle § 6 odst. 4 zákona o daních z příjmů podléhá příjem srážkové dani, pokud
    u zaměstnavatele není podepsané prohlášení k dani a úhrn příjmů u téhož
    zaměstnavatele nedosáhne částky rozhodné pro účast na nemocenském pojištění.

    Model oproti zákonu zjednodušuje: příjem z pracovního poměru srážkové dani
    nepodléhá. Podrobnosti u sdílené funkce podleha_prijem_srazkove_dani.
    """

    def formula(osoba, period, parameters):
        return podleha_prijem_srazkove_dani(osoba, period, parameters, 1)
