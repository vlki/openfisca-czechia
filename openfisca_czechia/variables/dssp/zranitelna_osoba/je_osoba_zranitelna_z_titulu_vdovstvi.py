from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_vdovstvi(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu vdovství v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        # § 7 odst. 1 i) Zranitelnou osobou je pozůstalý manžel nebo partner, se kterým uzavřel
        # partnerství podle občanského zákoníku nebo registrované partnerství podle zákona
        # o registrovaném partnerství (dále jen „partner“), a to po dobu 12 kalendářních měsíců
        # od měsíce následujícího po měsíci, kdy jeho manžel nebo partner zemřel
        return False
