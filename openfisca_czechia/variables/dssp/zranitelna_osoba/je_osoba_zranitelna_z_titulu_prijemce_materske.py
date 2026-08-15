from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_prijemce_materske(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu příjemce mateřské v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        materska = osoba("materska", period)

        # § 7 odst. 1 d) Zranitelnou osobou je osoba pobírající peněžitou pomoc v mateřství
        # nebo nemocenské poskytované v souvislosti s porodem.
        # Pozn. nemocenskou poskytovanou v souvislosti s porodem zde aktuálně ignorujeme
        return materska > 0
