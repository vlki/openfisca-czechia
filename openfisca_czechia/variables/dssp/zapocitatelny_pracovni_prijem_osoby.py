from openfisca_core.model_api import max_
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_zapocitatelny_pracovni_prijem_osoby(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Započitatelný pracovní příjem osoby pro DSSP"
    documentation = """
    Příjem ze závislé činnosti se do rozhodného příjmu započítává po odpočtu
    pojistného a daně připadající na tento příjem (§ 4 odst. 2 zákona 151/2025 Sb.).
    U nízkých příjmů může odpočet převýšit samotný příjem, typicky kvůli doplatku
    do minimálního zdravotního pojištění -- osobě s hrubou mzdou 1 000 Kč vychází
    v roce 2026 čistý pracovní příjem -2 005 Kč.

    Záporná hodnota ale do rozhodného příjmu vstoupit nemůže. Podle § 4 odst. 3
    zákona 151/2025 Sb. se každý z příjmů započítává samostatně a žádný z nich
    nelze snížit o ztrátu z jiného druhu příjmů. Kdyby se záporný pracovní příjem
    sčítal s ostatními, ukrojil by například z důchodu jiného člena domácnosti.
    Stejně to vychází i z daňové konstrukce, na kterou § 4 odst. 1 písm. a) bod 1
    odkazuje: dílčí základ daně ze závislé činnosti podle § 6 zákona o daních
    z příjmů záporný být nemůže, daňová ztráta vzniká jen podle § 7 a § 9.

    Proto se příjem omezuje zdola na nule. Omezení je na úrovni osoby, protože
    měsíční příjem domácnosti je součtem měsíčních příjmů jejích členů
    (§ 2 odst. 4 zákona 151/2025 Sb.).

    Mimo DSSP se záporný čistý pracovní příjem nechává být -- u srážek v exekuci
    i u čistého peněžního příjmu domácnosti jde o reálný peněžní tok.
    """

    def formula(osoba, period, parameters):
        cisty_pracovni_prijem_osoby_bez_danoveho_bonusu = osoba(
            "cisty_pracovni_prijem_osoby_bez_danoveho_bonusu", period
        )

        return max_(cisty_pracovni_prijem_osoby_bez_danoveho_bonusu, 0)
