import numpy as np

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class dssp(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Výše DSSP (dávky státní sociální pomoci)"

    def formula(domacnost, period, parameters):
        slozka_na_bydleni = domacnost("dssp_slozka_na_bydleni", period)
        slozka_na_zivobyti = domacnost("dssp_slozka_na_zivobyti", period)
        bonus_na_dite = domacnost("dssp_bonus_na_dite", period)
        pracovni_bonus = domacnost("dssp_pracovni_bonus", period)

        return np.ceil(
            slozka_na_bydleni + slozka_na_zivobyti + bonus_na_dite + pracovni_bonus
        )
