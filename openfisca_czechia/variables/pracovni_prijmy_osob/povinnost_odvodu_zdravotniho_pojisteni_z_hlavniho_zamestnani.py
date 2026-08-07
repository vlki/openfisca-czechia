from openfisca_core.model_api import select
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba
from openfisca_czechia.variables.pracovni_prijmy_osob.typ_pracovni_smlouvy_hlavniho_zamestnani import (
    TypPracovniSmlouvy,
)


class povinnost_odvodu_zdravotniho_pojisteni_z_hlavniho_zamestnani(Variable):
    value_type = bool
    entity = Osoba
    definition_period = MONTH
    label = "Povinnost odvodů zdravotního pojištění z hlavního zaměstnání"

    def formula(person, period, parameters):
        typ_pracovni_smlouvy = person(
            "typ_pracovni_smlouvy_hlavniho_zamestnani", period
        )
        hruby_prijem = person("hruby_prijem_z_hlavniho_zamestnani", period)

        hranice_dpp = parameters(
            period
        ).zdravotni_pojisteni.hranice_u_dpp_pro_povinnost_odvodu
        hranice_dpc = parameters(
            period
        ).zdravotni_pojisteni.hranice_u_dpc_pro_povinnost_odvodu

        return select(
            [
                hruby_prijem <= 0,
                typ_pracovni_smlouvy == TypPracovniSmlouvy.hpp,
                typ_pracovni_smlouvy == TypPracovniSmlouvy.dpp,
                typ_pracovni_smlouvy == TypPracovniSmlouvy.dpc,
            ],
            [False, True, hruby_prijem >= hranice_dpp, hruby_prijem >= hranice_dpc],
        )
