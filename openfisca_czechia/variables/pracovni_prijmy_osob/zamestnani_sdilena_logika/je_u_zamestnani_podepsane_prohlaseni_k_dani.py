from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.zamestnavatel import (
    Zamestnavatel,
)


def je_u_zamestnani_podepsane_prohlaseni_k_dani(osoba, period, index):
    """Zda je u zaměstnavatele daného zaměstnání podepsané prohlášení k dani.

    Prohlášení k dani lze podle § 38k odst. 6 zákona o daních z příjmů učinit za
    stejný kalendářní měsíc jen u jednoho plátce daně, proto je v modelu jedna
    proměnná na úrovni osoby.
    """
    podepsane_prohlaseni = osoba("podepsane_prohlaseni_u_zamestnavatele", period)

    return (podepsane_prohlaseni != Zamestnavatel.zadny) & (
        osoba(f"zamestnavatel_zamestnani_{index}", period) == podepsane_prohlaseni
    )
