import numpy as np

from openfisca_czechia.variables.pracovni_prijmy_osob.zamestnani_sdilena_logika.zaokrouhleny_zaklad_pro_zalohu import (
    zaokrouhleny_zaklad_pro_zalohu,
)


def zaloha_pred_slevami(zaklad, period, parameters):
    """Záloha na daň z příjmu ze zadaného základu, před uplatněním slev.

    Sazby a jejich hranice podle § 38h odst. 2, zaokrouhlení zálohy na celé
    koruny nahoru podle § 38h odst. 3.
    """
    zaklad_po_zaokrouhleni = zaokrouhleny_zaklad_pro_zalohu(zaklad)

    prumerna_hruba_mesicni_mzda_predchozi_rok = parameters(
        period.last_year
    ).prumerna_hruba_mesicni_mzda

    parametry_sazeb = parameters(period).dpfo.sazby

    hranice_vyssi_sazby_dane_jako_rocni_castka = (
        parametry_sazeb.hranice_vyssi_sazby * prumerna_hruba_mesicni_mzda_predchozi_rok
    )
    hranice_vyssi_sazby_dane_jako_mesicni_castka = (
        hranice_vyssi_sazby_dane_jako_rocni_castka / 12
    )

    cast_prijmu_pod_hranici = np.minimum(
        zaklad_po_zaokrouhleni, hranice_vyssi_sazby_dane_jako_mesicni_castka
    )
    cast_prijmu_nad_hranici = np.maximum(
        zaklad_po_zaokrouhleni - hranice_vyssi_sazby_dane_jako_mesicni_castka, 0
    )

    # Záloha se zaokrouhluje na celé koruny nahoru. Nejdříve děláme zaokrouhlení
    # na 2 desetinná místa, abychom odstranili artefakty po násobení floatů.
    return np.ceil(
        np.round(
            cast_prijmu_pod_hranici * parametry_sazeb.zakladni_sazba
            + cast_prijmu_nad_hranici * parametry_sazeb.vyssi_sazba,
            decimals=2,
        )
    )
