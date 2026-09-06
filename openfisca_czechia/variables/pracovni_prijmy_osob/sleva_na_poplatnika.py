from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class sleva_na_poplatnika(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Měsíční sleva na dani na poplatníka"
    documentation = """
    Sleva podle § 35ba odst. 1 písm. a) zákona o daních z příjmů. Uplatní se jen
    ze zálohy u zaměstnavatele, u kterého je podepsané prohlášení k dani, a nejvýše
    do nuly.
    """

    def formula(osoba, period, parameters):
        return osoba.filled_array(parameters(period).dpfo.sleva_na_poplatnika)
