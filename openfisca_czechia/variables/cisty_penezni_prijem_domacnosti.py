from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class cisty_penezni_prijem_domacnosti(Variable):
    value_type = float
    entity = Domacnost
    definition_period = MONTH
    label = "Čistý peněžní příjem domácnosti"

    def formula(domacnost, period, parameters):
        ciste_pracovni_prijmy_osob_v_domacnosti = domacnost(
            "ciste_pracovni_prijmy_osob_v_domacnosti", period
        )

        materska = domacnost.sum(domacnost.members("materska", period))
        rodicovsky_prispevek = domacnost.sum(
            domacnost.members("rodicovsky_prispevek", period)
        )
        vyzivne_na_deti = domacnost.sum(domacnost.members("vyzivne_na_deti", period))

        starobni_duchod = domacnost.sum(domacnost.members("starobni_duchod", period))
        invalidni_vdovecky_sirotci_duchody = domacnost.sum(
            domacnost.members("invalidni_vdovecky_sirotci_duchody", period)
        )
        nemocenska = domacnost.sum(domacnost.members("nemocenska", period))
        odmena_pestouna = domacnost.sum(domacnost.members("odmena_pestouna", period))
        podpora_v_nezamestnanosti = domacnost.sum(
            domacnost.members("podpora_v_nezamestnanosti", period)
        )
        prispevek_na_peci = domacnost.sum(
            domacnost.members("prispevek_na_peci", period)
        )
        prispevek_na_uhradu_potreb_na_dite = domacnost.sum(
            domacnost.members("prispevek_na_uhradu_potreb_na_dite", period)
        )

        jine_prijmy = domacnost.sum(domacnost.members("jine_prijmy", period))

        dssp = domacnost("dssp", period)

        return (
            ciste_pracovni_prijmy_osob_v_domacnosti
            + materska
            + rodicovsky_prispevek
            + vyzivne_na_deti
            + starobni_duchod
            + invalidni_vdovecky_sirotci_duchody
            + nemocenska
            + odmena_pestouna
            + podpora_v_nezamestnanosti
            + prispevek_na_peci
            + prispevek_na_uhradu_potreb_na_dite
            + jine_prijmy
            + dssp
        )
