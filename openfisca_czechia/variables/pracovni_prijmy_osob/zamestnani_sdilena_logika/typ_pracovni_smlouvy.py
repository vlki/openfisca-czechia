from openfisca_core.indexed_enums import Enum


class TypPracovniSmlouvy(Enum):
    __order__ = "hpp dpp dpc"
    hpp = "Hlavní pracovní poměr"
    dpp = "Dohoda o provedení práce"
    dpc = "Dohoda o pracovní činnosti"
