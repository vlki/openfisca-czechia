from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class prijem_u_zamestnavatele_s_podepsanym_prohlasenim(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Hrubý příjem u zaměstnavatele, u kterého je podepsané prohlášení k dani"
    documentation = """
    Na tomto úhrnu se podle § 35d odst. 4 zákona o daních z příjmů testuje nárok
    na měsíční daňový bonus. Příjmy zdaněné srážkou se do něj nezapočítávají,
    což je splněno automaticky: u zaměstnavatele s podepsaným prohlášením srážková
    daň nikdy nenastává.
    """

    def formula(osoba, period, parameters):
        prijem = 0.0
        for index in INDEXY_ZAMESTNANI:
            je_podepsane_prohlaseni = osoba(
                f"je_podepsane_prohlaseni_k_dani_u_zamestnani_{index}", period
            )
            prijem = prijem + where(
                je_podepsane_prohlaseni,
                osoba(f"hruby_prijem_ze_zamestnani_{index}", period),
                0,
            )

        return prijem
