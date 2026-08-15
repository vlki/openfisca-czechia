from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_nezaopatreneho_ditete(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu nezaopatřeného dítěte v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        je_nezaopatrene_dite = osoba("je_nezaopatrene_dite", period)

        # § 7 odst. 1 h) Zranitelnou osobou je nezaopatřené dítě
        return je_nezaopatrene_dite
