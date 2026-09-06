from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class sleva_na_prukaz_ztpp(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Měsíční sleva na dani na průkaz ZTP/P"
    documentation = """
    Sleva podle § 35ba odst. 1 písm. e) zákona o daních z příjmů. Lze ji kombinovat
    se slevou na invaliditu. Uplatní se jen ze zálohy u zaměstnavatele, u kterého
    je podepsané prohlášení k dani, a nejvýše do nuly.
    """

    def formula(osoba, period, parameters):
        ma_prukaz_ztpp = osoba("ma_prukaz_ztpp", period)

        return where(ma_prukaz_ztpp, parameters(period).dpfo.sleva_na_prukaz_ztpp, 0)
