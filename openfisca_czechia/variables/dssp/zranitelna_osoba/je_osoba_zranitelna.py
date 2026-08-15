from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Osoba


class dssp_je_osoba_zranitelna(Variable):
    value_type = bool
    entity = Osoba
    label = "Zda je osoba zranitelná v rámci DSSP"
    definition_period = MONTH
    default_value = True

    def formula(osoba, period, parameters):
        je_osoba_zranitelna_z_titulu_veku = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_veku", period
        )
        je_osoba_zranitelna_z_titulu_prijemce_starobniho_duchodu = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_prijemce_starobniho_duchodu", period
        )
        je_osoba_zranitelna_z_titulu_invalidity = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_invalidity", period
        )
        je_osoba_zranitelna_z_titulu_prijemce_materske = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_prijemce_materske", period
        )
        je_osoba_zranitelna_z_titulu_pecujiciho_rodice = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_pecujiciho_rodice", period
        )
        je_osoba_zranitelna_z_titulu_pece_o_osobu_zavislou_na_pomoci_jine_osoby = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_pece_o_osobu_zavislou_na_pomoci_jine_osoby",
            period,
        )
        je_osoba_zranitelna_z_titulu_pozivatele_prispevku_na_peci = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_pozivatele_prispevku_na_peci", period
        )
        je_osoba_zranitelna_z_titulu_nezaopatreneho_ditete = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_nezaopatreneho_ditete", period
        )
        je_osoba_zranitelna_z_titulu_vdovstvi = osoba(
            "dssp_je_osoba_zranitelna_z_titulu_vdovstvi", period
        )

        return (
            je_osoba_zranitelna_z_titulu_veku
            | je_osoba_zranitelna_z_titulu_prijemce_starobniho_duchodu
            | je_osoba_zranitelna_z_titulu_invalidity
            | je_osoba_zranitelna_z_titulu_prijemce_materske
            | je_osoba_zranitelna_z_titulu_pecujiciho_rodice
            | je_osoba_zranitelna_z_titulu_pece_o_osobu_zavislou_na_pomoci_jine_osoby
            | je_osoba_zranitelna_z_titulu_pozivatele_prispevku_na_peci
            | je_osoba_zranitelna_z_titulu_nezaopatreneho_ditete
            | je_osoba_zranitelna_z_titulu_vdovstvi
        )
