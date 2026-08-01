from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dalsi_poplatky_spojene_s_bydlenim(Variable):
    value_type = float
    entity = Domacnost
    label = "Další poplatky domácnosti spojené s bydlením"
    definition_period = MONTH
    default_value = 0
