from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp_pocet_osob_v_domacnosti_pro_vypocet_nakladu_na_bydleni(Variable):
    value_type = int
    entity = Domacnost
    definition_period = MONTH
    label = "Počet osob v domácnosti pro výpočet nákladů na bydlení"

    def formula(domacnost, period, parameters):
        zranitelne_osoby = domacnost.members("dssp_je_osoba_zranitelna", period)
        pracovne_aktivni_osoby = domacnost.members(
            "dssp_je_osoba_pracovne_aktivni", period
        )

        return domacnost.sum(zranitelne_osoby | pracovne_aktivni_osoby)
