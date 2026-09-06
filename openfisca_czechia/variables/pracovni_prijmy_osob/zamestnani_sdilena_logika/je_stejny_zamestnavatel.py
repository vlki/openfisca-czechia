def je_stejny_zamestnavatel(osoba, period, index, jiny_index):
    """Zda jsou obě zaměstnání u téhož zaměstnavatele."""
    return osoba(f"zamestnavatel_zamestnani_{index}", period) == osoba(
        f"zamestnavatel_zamestnani_{jiny_index}", period
    )
