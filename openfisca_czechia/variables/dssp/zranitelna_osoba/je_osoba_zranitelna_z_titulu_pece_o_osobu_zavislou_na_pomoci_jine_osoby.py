from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna_z_titulu_pece_o_osobu_zavislou_na_pomoci_jine_osoby(
    Variable
):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná z titulu péče o osobu závislou na pomoci jiné osoby v rámci DSSP"
    definition_period = MONTH
    default_value = False

    def formula(osoba, period, parameters):
        pecovatel_uvedeny_v_prispevku_na_peci = osoba(
            "pecovatel_uvedeny_v_prispevku_na_peci", period
        )

        # § 7 odst. 1 f) Zranitelnou osobou je osoba osobně pečující o dítě ve věku do 10 let
        # závislé na pomoci jiné osoby ve stupni I nebo osoba osobně pečující o osobu závislou
        # na pomoci jiné osoby ve stupni II nebo vyšším, a to pokud v žádosti o příspěvek na
        # péči byla uvedena nebo po přiznání příspěvku na péči příslušnému orgánu ohlášena jako
        # osoba poskytující pomoc
        return pecovatel_uvedeny_v_prispevku_na_peci
