from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class vyjimka_z_minimalniho_zdravotniho_pojisteni(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    default_value = False
    label = "Výjimka z minimálního zdravotního pojištění"
    documentation = """
    Podle § 3 odst. 8 zákona č. 592/1992 Sb. se minimální vyměřovací základ nevztahuje
    na vyjmenované zaměstnance, a to pokud u nich důvod trvá po celý kalendářní měsíc.
    Přehled vede např. VZP:
    https://www.vzp.cz/platci/informace/zamestnavatel/vymerovaci-zaklad-a-vypocet-pojistneho/pro-koho-neplati-povinnost-dodrzet-minimalni-vymerovaci-zaklad

    Model z toho pokrývá:

    1. osoby, za které platí pojistné stát -- plati_stat_zdravotni_pojisteni,
    2. držitele průkazu ZTP/P -- ma_prukaz_ztpp.

    Nepokrývá:

    3. osoby s průkazem ZTP; model teď rozlišuje jen ZTP/P,
    4. osoby, které dosáhly věku pro nárok na starobní důchod, ale nesplňují další
       podmínky pro jeho přiznání; model teď nemá, čím tento stav rozpoznat,
    5. osoby souběžně vykonávající samostatnou výdělečnou činnost a odvádějící z ní
       zálohy aspoň z minimálního vyměřovacího základu; model příjmy z podnikání zatím
       neobsahuje.

    U bodů 3 až 5 tedy model dopočte doplatek do minima, který podle zákona vzniknout
    nemá. Bod „osoby, které jsou pouze příjemcem odměny pěstouna" tu záměrně není:
    kdo má jen odměnu pěstouna, nemá zaměstnání, ze kterého by doplatek vznikal, takže
    by ta podmínka nemohla nic změnit.

    Proměnná zůstává vstupem, takže explicitně zadaná hodnota tuto formuli přebije.
    """

    def formula(osoba, period, parameters):
        plati_stat_zdravotni_pojisteni = osoba("plati_stat_zdravotni_pojisteni", period)
        ma_prukaz_ztpp = osoba("ma_prukaz_ztpp", period)

        return plati_stat_zdravotni_pojisteni | ma_prukaz_ztpp
