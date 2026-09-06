"""Identita zaměstnavatele jednotlivých zaměstnání.

Zaměstnavatel je Enum, ne volný text: jeho identita řídí seskupování příjmů pro
limity odvodů, pro srážkovou daň i pro výpočet zálohy na daň, takže překlep ve
volném textu by tiše změnil výslednou daň. Volný název zaměstnavatele je v modelu
jako ``nazev_zamestnavatele_zamestnani_i``, ale do výpočtu nevstupuje.

Hodnota ``zadny`` dává smysl jen u proměnné
``podepsane_prohlaseni_u_zamestnavatele``, kde znamená, že poplatník prohlášení
k dani neučinil u žádného zaměstnavatele.
"""

from openfisca_core.indexed_enums import Enum


class Zamestnavatel(Enum):
    __order__ = "zamestnavatel_a zamestnavatel_b zamestnavatel_c zadny"
    zamestnavatel_a = "Zaměstnavatel A"
    zamestnavatel_b = "Zaměstnavatel B"
    zamestnavatel_c = "Zaměstnavatel C"
    zadny = "Žádný"
