import numpy as np

from openfisca_core.model_api import where
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.indexy_zamestnani import (
    INDEXY_ZAMESTNANI,
)


class doplatek_do_minimalniho_zdravotniho_pojisteni(Variable):
    value_type = float
    entity = Osoba
    definition_period = MONTH
    label = "Doplatek do minimálního zdravotního pojištění"
    documentation = """
    Minimální vyměřovací základ je pojem na úrovni pojištěnce, ne jednotlivého
    zaměstnání. Při více zaměstnavatelích se vyměřovací základy sčítají a doplatek
    se odvádí prostřednictvím jednoho zvoleného zaměstnavatele. Pokud má
    zaměstnanec příjem pod minimální mzdou a neplatí pro něj výjimka z minimálního
    zdravotního pojištění, strhává se mu z mzdy taková částka, aby výsledný odvod
    odpovídal minimální výši zdravotního pojištění. Počítá se tak, že se vezme
    rozdíl mezi minimální mzdou a vyměřovacím základem zaměstnance a z něho se
    vezme podíl pomocí součtu sazeb zaměstnance a zaměstnavatele.
    """

    def formula(osoba, period, parameters):
        vyjimka_z_minimalniho_pojisteni = osoba(
            "vyjimka_z_minimalniho_zdravotniho_pojisteni", period
        )

        vymerovaci_zaklad = 0.0
        ma_zamestnani_s_povinnosti_odvodu = False
        for index in INDEXY_ZAMESTNANI:
            povinnost_odvodu = osoba(
                f"povinnost_odvodu_zdravotniho_pojisteni_ze_zamestnani_{index}", period
            )
            vymerovaci_zaklad = vymerovaci_zaklad + where(
                povinnost_odvodu,
                osoba(f"hruby_prijem_ze_zamestnani_{index}", period),
                0,
            )
            ma_zamestnani_s_povinnosti_odvodu = (
                ma_zamestnani_s_povinnosti_odvodu | povinnost_odvodu
            )

        sazba_zamestnance = parameters(
            period
        ).zdravotni_pojisteni.sazby.sazba_zamestnance
        sazba_zamestnavatele = parameters(
            period
        ).zdravotni_pojisteni.sazby.sazba_zamestnavatele
        minimalni_mzda = parameters(period).minimalni_mzda

        celkova_sazba_zamestnance_i_zamestnavatele = (
            sazba_zamestnance + sazba_zamestnavatele
        )

        return where(
            (
                ma_zamestnani_s_povinnosti_odvodu
                & ~vyjimka_z_minimalniho_pojisteni
                & (vymerovaci_zaklad < minimalni_mzda)
            ),
            # Zaokrouhluje se na koruny nahoru. Nejdřív děláme round na 2 desetinná
            # místa, aby se odstranily artefakty po násobení Python float čísel
            np.ceil(
                np.round(
                    (minimalni_mzda - vymerovaci_zaklad)
                    * celkova_sazba_zamestnance_i_zamestnavatele,
                    decimals=2,
                )
            ),
            0.0,
        )
