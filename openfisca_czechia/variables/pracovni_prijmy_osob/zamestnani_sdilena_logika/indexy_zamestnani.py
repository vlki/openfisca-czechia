"""Indexy slotů zaměstnání.

Model umožňuje zadat u jedné osoby až tři souběžná zaměstnání. Proměnné
jednotlivých zaměstnání jsou natvrdo definované v podsložkách ``zamestnani_1``,
``zamestnani_2`` a ``zamestnani_3``. Generovat je programově nejde -- OpenFisca
soubor s proměnnou parsuje přes ``ast`` a hledá v něm doslovnou definici třídy.

Logika, která se dívá napříč sloty, je proto v této složce, aby definice
v jednotlivých slotech zůstaly co nejtenčí a jejich trojí opakování bylo nudné.
"""

INDEXY_ZAMESTNANI = (1, 2, 3)
