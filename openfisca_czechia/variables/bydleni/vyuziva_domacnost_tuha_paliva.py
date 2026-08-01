from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class vyuziva_domacnost_tuha_paliva(Variable):
    value_type = bool
    entity = Domacnost
    label = "Využívá domácnost tuhá paliva"
    definition_period = MONTH
