from openfisca_core.model_api import select
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.stupen_invalidity import StupenInvalidity


class sleva_na_invaliditu(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Měsíční sleva na dani na invaliditu"
    documentation = """
    Sleva podle § 35ba odst. 1 písm. c) a d) zákona o daních z příjmů. Uplatní se
    jen ze zálohy u zaměstnavatele, u kterého je podepsané prohlášení k dani,
    a nejvýše do nuly.
    """

    def formula(osoba, period, parameters):
        stupen_invalidity = osoba("stupen_invalidity", period)

        castky_slevy = parameters(period).dpfo.sleva_na_invaliditu

        return select(
            [
                stupen_invalidity == StupenInvalidity.stupen_1,
                stupen_invalidity == StupenInvalidity.stupen_2,
                stupen_invalidity == StupenInvalidity.stupen_3,
            ],
            [
                castky_slevy.stupen_1,
                castky_slevy.stupen_2,
                castky_slevy.stupen_3,
            ],
            default=0,
        )
