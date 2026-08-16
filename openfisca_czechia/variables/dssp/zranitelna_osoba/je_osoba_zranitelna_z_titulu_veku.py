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
        vek = osoba("vek", period)

        vek_od_ktereho_je_osoba_zranitelna = parameters(
            period
        ).dssp.zranitelna_osoba.zranitelna_osoba_z_titulu_veku

        # § 7 odst. 1 a) Zranitelnou osobou je osoba starší 68 let
        return vek >= vek_od_ktereho_je_osoba_zranitelna
