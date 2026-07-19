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
        # vyjimka_z_minimalniho_pojisteni = person(
        #     "vyjimka_z_minimalniho_zdravotniho_pojisteni", period
        # )
        hruby_prijem = person("hruby_prijem_z_hlavniho_zamestnani", period)

        # minimalni_mzda = parameters(period).minimalni_mzda
        sazba_zamestnance = parameters(
            period
        ).zdravotni_pojisteni.sazby.sazba_zamestnance

        # TODO: pridat minimalni zdravotni pojisteni
        return where(
            povinnost_odvodu,
            np.ceil(np.round(hruby_prijem * sazba_zamestnance, decimals=10)),
            0.0,
        )
