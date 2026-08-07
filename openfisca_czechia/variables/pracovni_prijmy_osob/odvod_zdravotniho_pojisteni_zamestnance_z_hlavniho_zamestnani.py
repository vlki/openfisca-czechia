import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class odvod_zdravotniho_pojisteni_zamestnance_z_hlavniho_zamestnani(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Výše odvodu zdravotního pojištění z hlavního zaměstnání"

    def formula(person, period, parameters):
        povinnost_odvodu = person(
            "povinnost_odvodu_zdravotniho_pojisteni_z_hlavniho_zamestnani", period
        )
        vyjimka_z_minimalniho_pojisteni = person(
            "vyjimka_z_minimalniho_zdravotniho_pojisteni", period
        )
        hruby_prijem = person("hruby_prijem_z_hlavniho_zamestnani", period)

        sazba_zamestnance = parameters(
            period
        ).zdravotni_pojisteni.sazby.sazba_zamestnance
        sazba_zamestnavatele = parameters(
            period
        ).zdravotni_pojisteni.sazby.sazba_zamestnavatele
        minimalni_mzda = parameters(period).minimalni_mzda

        odvod_zdravotniho_pojisteni = where(
            povinnost_odvodu,
            # Zaokrouhluje se na koruny nahoru. Nejdřív děláme round na 2 desetinná
            # místa, aby se odstranily artefakty po násobení Python float čísel
            np.ceil(np.round(hruby_prijem * sazba_zamestnance, decimals=2)),
            0.0,
        )

        # Pokud má zaměstnanec příjem pod minimální mzdou a neplatí pro něj výjimka
        # z minimálního zdravotního pojištění, pak se z jeho mzdy strhává taková částka,
        # aby výsledný odvod odpovídal minimální výši zdravotního pojištění. Počítá se to
        # tak, že se vezme rozdíl mezi minimální mzdou a mzdou zaměstnance a z něho se
        # vezme podíl pomocí součtu sazeb zaměstnance a zaměstnavatele.
        celkova_sazba_zamestnance_i_zamestnavatele = (
            sazba_zamestnance + sazba_zamestnavatele
        )
        doplatek_kdyz_prijem_pod_minimalni_mzdou = where(
            (
                (hruby_prijem < minimalni_mzda)
                & povinnost_odvodu
                & ~vyjimka_z_minimalniho_pojisteni
            ),
            # Zaokrouhluje se na koruny nahoru. Nejdřív děláme round na 2 desetinná
            # místa, aby se odstranily artefakty po násobení Python float čísel
            np.ceil(
                np.round(
                    (minimalni_mzda - hruby_prijem)
                    * celkova_sazba_zamestnance_i_zamestnavatele
                )
            ),
            0,
        )

        return odvod_zdravotniho_pojisteni + doplatek_kdyz_prijem_pod_minimalni_mzdou
