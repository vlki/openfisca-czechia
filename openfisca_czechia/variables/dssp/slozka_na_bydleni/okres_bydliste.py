from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_czechia.entities import Domacnost


class DsspOkresBydliste(Enum):
    # Hlavní město Praha
    praha = "Hlavní město Praha"
    # Jihomoravský kraj
    blansko = "Blansko"
    brno_mesto = "Brno-město"
    brno_venkov = "Brno-venkov"
    breclav = "Břeclav"
    hodonin = "Hodonín"
    vyskov = "Vyškov"
    znojmo = "Znojmo"
    # Jihočeský kraj
    jindrichuv_hradec = "Jindřichův Hradec"
    prachatice = "Prachatice"
    pisek = "Písek"
    strakonice = "Strakonice"
    tabor = "Tábor"
    ceske_budejovice = "České Budějovice"
    cesky_krumlov = "Český Krumlov"
    # Karlovarský kraj
    cheb = "Cheb"
    karlovy_vary = "Karlovy Vary"
    sokolov = "Sokolov"
    # Kraj Vysočina
    havlickuv_brod = "Havlíčkův Brod"
    jihlava = "Jihlava"
    pelhrimov = "Pelhřimov"
    trebic = "Třebíč"
    zdar_nad_sazavou = "Žďár nad Sázavou"
    # Královéhradecký kraj
    hradec_kralove = "Hradec Králové"
    jicin = "Jičín"
    nachod = "Náchod"
    rychnov_nad_kneznou = "Rychnov nad Kněžnou"
    trutnov = "Trutnov"
    # Liberecký kraj
    jablonec_nad_nisou = "Jablonec nad Nisou"
    liberec = "Liberec"
    semily = "Semily"
    ceska_lipa = "Česká Lípa"
    # Moravskoslezský kraj
    bruntal = "Bruntál"
    frydek_mistek = "Frýdek-Místek"
    karvina = "Karviná"
    novy_jicin = "Nový Jičín"
    opava = "Opava"
    ostrava_mesto = "Ostrava-město"
    # Olomoucký kraj
    jesenik = "Jeseník"
    olomouc = "Olomouc"
    prostejov = "Prostějov"
    prerov = "Přerov"
    sumperk = "Šumperk"
    # Pardubický kraj
    chrudim = "Chrudim"
    pardubice = "Pardubice"
    svitavy = "Svitavy"
    usti_nad_orlici = "Ústí nad Orlicí"
    # Plzeňský kraj
    domazlice = "Domažlice"
    klatovy = "Klatovy"
    plzen_jih = "Plzeň-jih"
    plzen_mesto = "Plzeň-město"
    plzen_sever = "Plzeň-sever"
    rokycany = "Rokycany"
    tachov = "Tachov"
    # Středočeský kraj
    benesov = "Benešov"
    beroun = "Beroun"
    kladno = "Kladno"
    kolin = "Kolín"
    kutna_hora = "Kutná Hora"
    mlada_boleslav = "Mladá Boleslav"
    melnik = "Mělník"
    nymburk = "Nymburk"
    praha_vychod = "Praha-východ"
    praha_zapad = "Praha-západ"
    pribram = "Příbram"
    rakovnik = "Rakovník"
    # Zlínský kraj
    kromeriz = "Kroměříž"
    uherske_hradiste = "Uherské Hradiště"
    vsetin = "Vsetín"
    zlin = "Zlín"
    # Ústecký kraj
    chomutov = "Chomutov"
    decin = "Děčín"
    litomerice = "Litoměřice"
    louny = "Louny"
    most = "Most"
    teplice = "Teplice"
    usti_nad_labem = "Ústí nad Labem"


class dssp_okres_bydliste(Variable):
    value_type = Enum
    possible_values = DsspOkresBydliste
    default_value = DsspOkresBydliste.praha
    entity = Domacnost
    definition_period = MONTH
    label = "Okres bydliště pro DSSP"
