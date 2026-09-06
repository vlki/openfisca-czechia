import numpy as np

from openfisca_core.model_api import where

# § 38h odst. 1 zákona o daních z příjmů: základ pro výpočet zálohy se do této
# částky zaokrouhluje na celé koruny nahoru, nad ni na celé stokoruny nahoru.
HRANICE_ZAOKROUHLENI_ZAKLADU_ZALOHY = 100


def zaokrouhleny_zaklad_pro_zalohu(zaklad):
    """Zaokrouhlení základu pro výpočet zálohy podle § 38h odst. 1.

    Základ do 100 Kč se zaokrouhluje na celé koruny nahoru, nad 100 Kč na celé
    stokoruny nahoru. Nejdřív děláme round na 2 desetinná místa, aby se
    odstranily artefakty po dělení Python float čísel.
    """
    return where(
        zaklad <= HRANICE_ZAOKROUHLENI_ZAKLADU_ZALOHY,
        np.ceil(np.round(zaklad, decimals=2)),
        np.ceil(np.round(zaklad / 100, decimals=2)) * 100,
    )
