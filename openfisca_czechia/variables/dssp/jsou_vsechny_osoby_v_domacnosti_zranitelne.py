from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_jsou_vsechny_osoby_v_domacnosti_zranitelne(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Zda jsou všechny osoby v domácnosti zranitelné v rámci DSSP"

    def formula(domacnost, period, parameters):
        return domacnost.all(domacnost.members("dssp_je_osoba_zranitelna", period))
