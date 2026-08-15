from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_veku(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu věku v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        # § 7 odst. 1 a) Zranitelnou osobou je osoba starší 68 let
        # TODO
        return False
