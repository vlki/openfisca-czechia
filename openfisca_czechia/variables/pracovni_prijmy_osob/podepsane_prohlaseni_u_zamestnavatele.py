from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.zamestnavatel import (
    Zamestnavatel,
)


class podepsane_prohlaseni_u_zamestnavatele(Variable):
    value_type = Enum
    possible_values = Zamestnavatel
    default_value = Zamestnavatel.zamestnavatel_a
    entity = Osoba
    definition_period = MONTH
    label = "Zaměstnavatel, u kterého je podepsané prohlášení k dani z příjmu"
    documentation = """
    Prohlášení k dani lze podle § 38k odst. 6 zákona o daních z příjmů učinit za
    stejné období kalendářního měsíce jen u jednoho plátce daně. Jen u tohoto
    zaměstnavatele se ze zálohy na daň uplatňují měsíční slevy na dani a měsíční
    daňové zvýhodnění na vyživované děti.

    Hodnota zadny znamená, že poplatník prohlášení neučinil u žádného
    zaměstnavatele.
    """
